#!/usr/bin/python

from __future__ import division, print_function

import io
import os
import tempfile
import shutil
import re
import argparse

import subprocess
import tarfile

from itertools import groupby

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

import datetime
from time import strptime

from IPython.nbformat import current
from IPython.config import Config
from IPython.nbconvert import HTMLExporter
from IPython.nbconvert.filters.markdown import markdown2html_pandoc


class SimpleNamespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def itersplit(predicate, seq):
    return (tuple(g) for k,g in groupby(seq, key=lambda x: not predicate(x)) if
            k)


def date_to_edx(date, add_days=0):
    tmp = strptime(date, '%d %b %Y')

    date = datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, 12)
    date = date + datetime.timedelta(days=add_days)
    date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    return date


def parse_syllabus(syllabus_file, content_folder=''):
    standard_safe_date = "28 Feb 2030"
    # loading raw syllabus
    syll = split_into_units(syllabus_file)[0]
    cell = syll.worksheets[0].cells[1]

    def section_to_name_date(line):
        finddate = r' \(air date\: (.+?)\)'
        try:
            date = re.findall(finddate, line)[0]
            name = re.sub(finddate, '', line)
        except IndexError:
            date = standard_safe_date
            name = line
            print('Date unset in section {}'.format(line))
        return name, date

    def subs_to_name_file(line):
        try:
            file_name = re.findall(r'\((.+?\.ipynb)\)', line)[0]
        except IndexError:
            return
        subsection_name = re.findall(r'\[(.+?)\]', line)[0]
        return subsection_name, file_name

    is_section = lambda line: line.startswith('*')

    lines = cell['source'].split('\n')
    sections = [line.replace('*', '') for line
                in lines if is_section(line)]

    sections = [section_to_name_date(j) for j in sections]
    # Make a list of lines in each section.
    subsections = itersplit(is_section, lines)
    # Filter the actual subsections.
    subsections = [[subs_to_name_file(i) for i in j if subs_to_name_file(i) is
                    not None] for j in subsections]

    tmp = SimpleNamespace(category='main', chapters=[])
    for i, section in enumerate(zip(sections, subsections)):
        #creating chapter
        chapter = SimpleNamespace(category='chapter', sequentials=[])

        chapter.name = section[0][0]
        chapter.date = section[0][1]
        chapter.url  = "sec_{0}".format(str(i).zfill(2))

        for j, subsection in enumerate(section[1]):
            # creating sequential
            sequential = SimpleNamespace(category='sequential', verticals=[])

            sequential.name = subsection[0]
            sequential.date = chapter.date
            sequential.url = "subsec_{0}_{1}".format(str(i).zfill(2),
                                                     str(j).zfill(2))
            sequential.source_notebook = content_folder + '/' + subsection[1]

            chapter.sequentials.append(sequential)

        tmp.chapters.append(chapter)
    return tmp


def split_into_units(nb_name):
    """Split notebook into units."""
    try:
        with io.open(nb_name, 'r', encoding='utf-8') as f:
            nb = current.read(f, 'json')
    except IOError as e:
        if e.errno == 2:
            print('File not found: {0}'.format(nb_name))
            return []
        else:
            raise e
    indexes = []
    cells = nb.worksheets[0].cells
    for (i, cell) in enumerate(cells):
        if cell.cell_type == 'heading' and cell.level == 1:
            indexes.append(i)

    separated_cells = [cells[i:j] for i, j in zip(indexes, indexes[1:]+[None])]

    worksheets = map(lambda cells: current.new_worksheet(name=cells[0].source,
                                                         cells=cells),
                     separated_cells)
    units = map(lambda worksheet: current.new_notebook(name=worksheet.name,
                                                       worksheets=[worksheet]),
                worksheets)
    return units


def export_unit_to_html(unit):
    """Export unit into html format."""
    path = os.path.dirname(os.path.realpath(__file__))
    cfg = Config({'HTMLExporter':{'template_file':'basic_reduced',
                                  'template_path':['.',path],
                                  'filters':{'markdown2html':
                                             markdown2html_pandoc}}})
    exportHtml = HTMLExporter(config=cfg)
    (body, resources) = exportHtml.from_notebook_node(unit)
    body = re.sub(r'\\begin\{ *equation *\}', '\[', body)
    body = re.sub(r'\\end\{ *equation *\}', '\]', body)

    return body


def make_filename_valid(string):
    cleaned_up_filename = re.sub(r'[/\\:$%*?,"<>| ]', '', string)
    return cleaned_up_filename


def modify_text(text):
    s = "".join([c for c in text if re.match(r'\w', c)])
    return s


def save_html(body, target_path):
    """Save html body into edX course."""
    with io.open(target_path, 'w', encoding='utf-8') as f:
        f.write(body)


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    output = reparsed.toprettyxml(indent="  ")

    # output = str(output)
    return output[output.find("\n")+1:]


def save_xml(xml, path):
    with io.open(path, 'w', encoding='utf-8') as f:
        text = prettify(xml)
        text = re.sub(r"\$\$(.*?)\$\$", r"\[\1\]", text)
        text = re.sub(r"\$(.*?)\$", r"\(\1\)", text)
        f.write(text)


def convert_normal_cells(normal_cells):
    """ Convert normal_cells into html. """
    for cell in normal_cells:
        if cell.cell_type == 'markdown':
            cell.source = re.sub(r'\\begin\{ *equation *\}', '\[', cell.source)
            cell.source = re.sub(r'\\end\{ *equation *\}', '\]', cell.source)
    worksheet = current.new_worksheet(cells=normal_cells)
    tmp = current.new_notebook(worksheets=[worksheet])
    html = export_unit_to_html(tmp)
    return html


def convert_MoocVideo_to_xml(par):
    """ Convert video_cell with MoocVideo into xml. """
    xml = Element('video')
    for key in par.keys():
        xml.attrib[key] = str(par[key])

    return xml


def add_solution(el, text):
    """Add a solution xml to a problem."""
    sol = SubElement(el, 'solution')
    div = SubElement(sol, 'div')
    div.attrib['class'] = 'detailed-solution'
    title = SubElement(div, 'p')
    title.text = 'Explanation'
    content = SubElement(div, 'p')
    content.text = text


def convert_MoocCheckboxesAssessment_to_xml(par):
    """Convert checkbox assignment into xml. """
    xml = Element('problem')

    for key in ['display_name', 'max_attempts']:
        xml.attrib[key] = str(par[key])

    p = SubElement(xml, 'p')
    p.text = par['question']

    p = SubElement(xml, 'p')
    p.text = 'Select the answers that match'

    sub = SubElement(xml, 'choiceresponse')
    sub = SubElement(sub, 'checkboxgroup')
    sub.attrib['label'] = "Select the answers that match"
    sub.attrib['direction'] = "vertical"

    for i, ans in enumerate(par['answers']):
        choice = SubElement(sub, 'choice')
        if i in par['correct_answers']:
            choice.attrib['correct'] = 'true'
        else:
            choice.attrib['correct'] = 'false'
        choice.text = ans

    if 'explanation' in par:
        add_solution(xml, par['explanation'])

    return xml


def convert_MoocMultipleChoiceAssessment_to_xml(par):
    """ Convert multiple choice question into xml. """
    xml = Element('problem')

    for key in ['display_name', 'max_attempts']:
        xml.attrib[key] = str(par[key])

    p = SubElement(xml, 'p')
    p.text = par['question']

    p = SubElement(xml, 'p')
    p.text = 'Please select correct answer'

    sub = SubElement(xml, 'multiplechoiceresponse')
    sub = SubElement(sub, 'choicegroup')
    sub.attrib['label'] = "Please select correct answer"
    sub.attrib['type'] = "MultipleChoice"

    for i, ans in enumerate(par['answers']):
        choice = SubElement(sub, 'choice')
        if i == par['correct_answer']:
            choice.attrib['correct'] = 'true'
        else:
            choice.attrib['correct'] = 'false'
        choice.text = ans

    if 'explanation' in par:
        add_solution(xml, par['explanation'])

    return xml


def convert_MoocPeerAssessment_to_xml(par, date):
    #tree = ElementTree.parse('./templates/openassessment.xml')
    xml = ElementTree.fromstring(par['openassessment_peer'])
    #xml = tree.getroot()

    if par['url_name'] is not None:
        xml.attrib['url_name'] = par['url_name']

    assessment = xml.find('assessments').find('assessment')

    for name in ['must_be_graded_by', 'must_grade']:
        assessment.attrib[name] = str(par[name])

    xml.attrib['submission_start'] = date_to_edx(date, 0)
    xml.attrib['submission_due'] = date_to_edx(date, par['due'])

    assessment.attrib['start'] = date_to_edx(date, 0)
    assessment.attrib['due'] = date_to_edx(date, par['review_due'])

    return xml


def convert_MoocSelfAssessment_to_xml(par, date):
    xml = ElementTree.fromstring(par['openassessment_self'])

    if par['url_name'] is not None:
        xml.attrib['url_name'] = par['url_name']

    assessment = xml.find('assessments').find('assessment')

    xml.attrib['submission_start'] = date_to_edx(date, 0)
    xml.attrib['submission_due'] = date_to_edx(date, par['due'])

    assessment.attrib['start'] = date_to_edx(date, 0)
    assessment.attrib['due'] = date_to_edx(date, par['review_due'])

    return xml


def convert_MoocDiscussion_to_xml(par):
    xml = Element('discussion')
    for key in par.keys():
        xml.attrib[key] = par[key]

    return xml, par['discussion_id']


def convert_unit(unit, date):
    """ Convert unit into html and special xml componenets. """
    cells = unit.worksheets[0].cells

    unit_output = []
    normal_cells = []

    convert_specials = {'MoocVideo': convert_MoocVideo_to_xml,
                        'MoocPeerAssessment':
                        convert_MoocPeerAssessment_to_xml,
                        'MoocSelfAssessment':
                        convert_MoocSelfAssessment_to_xml,
                        'MoocCheckboxesAssessment':
                        convert_MoocCheckboxesAssessment_to_xml,
                        'MoocMultipleChoiceAssessment':
                        convert_MoocMultipleChoiceAssessment_to_xml,
                        'MoocDiscussion': convert_MoocDiscussion_to_xml}

    for cell in cells:
        # Markdown-like cell
        if cell.cell_type != 'code':
            normal_cells.append(cell)
            continue

        # Empty code cell
        if not hasattr(cell, 'outputs') or not cell.outputs:
            continue

        # Cells with mooc components, special processing required
        try:
            cell_text = cell.outputs[0].text
        except AttributeError:
            cell_text = ''

        special = False
        for i, j in convert_specials.items():
            if i in cell_text:
                if normal_cells:
                    html = convert_normal_cells(normal_cells)
                    unit_output.append(['html', html])
                    normal_cells = []

                par = eval(cell_text, {i: dict for i in convert_specials})
                try:
                    out = j(par)
                except TypeError:
                    out = j(par, date)

                if i != 'MoocDiscussion':
                    unit_output.append([i, out])
                else:
                    unit_output.append([i, out[0], out[1]])
                special = True
                break

        # Regular code cell
        if not special:
            normal_cells.append(cell)

    if normal_cells:
        html = convert_normal_cells(normal_cells)
        unit_output.append(['html', html])
        normal_cells = []

    return unit_output


def converter(mooc_folder, args):
    """ Do converting job. """
    # Basic info
    info_org='DelftX'
    info_course='TOPOCMx'
    info_display_name='Topology in Condensed Matter: Tying Quantum Knots'
    info_run='1T2015'
    info_start="2015-02-05T12:00:00Z"

    # Mooc content location
    content_folder = mooc_folder

    # Temporary locations
    dirpath = tempfile.mkdtemp() + '/' + info_run
    if args.debug:
        print('Temporary path: ', dirpath)

    # Copying edx_skeleton
    skeleton = content_folder + '/edx_skeleton'
    if os.path.exists(skeleton):
        shutil.copytree(skeleton, dirpath)
    else:
        'No edx skeleton!'
        return

    # Loading data from syllabus
    syllabus_nb = os.path.join(content_folder, 'syllabus.ipynb')
    data = parse_syllabus(syllabus_nb, content_folder)

    # saving syllabus
    syllabus = split_into_units(syllabus_nb)[0]
    cell = syllabus.worksheets[0].cells[1]
    cell['source'] = re.sub(r"(?<!!)\[(.*?)\]\(.*?\)", r"\1", cell['source'])
    syllabus_html = export_unit_to_html(syllabus)
    save_html(syllabus_html, os.path.join(dirpath, 'tabs', 'syllabus.html'))


    # course.xml in main folder
    xml_main_course = Element('course')
    xml_main_course.attrib['course'] = info_course
    xml_main_course.attrib['org'] = info_org
    xml_main_course.attrib['url_name'] = info_run

    save_xml(xml_main_course, os.path.join(dirpath,'course.xml'))

    # $run$.xml in 'course' folder
    xml_course = Element('course')
    xml_course.attrib['display_name'] = info_display_name
    xml_course.attrib['start'] = info_start

    for chapter in data.chapters:
        chapter_sub = SubElement(xml_course, 'chapter')
        chapter_sub.attrib['url_name'] = chapter.url

    wiki = SubElement(xml_course, 'wiki')
    wiki.attrib['slug'] = ".".join([info_org, info_course, info_run])

    save_xml(xml_course, os.path.join(dirpath,'course',info_run+'.xml'))

    # saving chapters xmls inside 'chapter' folder
    for chapter in data.chapters:
        chapter_xml = Element('chapter')
        chapter_xml.attrib['display_name'] = chapter.name
        chapter_xml.attrib['start'] = date_to_edx(chapter.date)

        for sequential in chapter.sequentials:
            sequential_sub = SubElement(chapter_xml, 'sequential')
            sequential_sub.attrib['url_name'] = sequential.url

        save_xml(chapter_xml,
                 os.path.join(dirpath,'chapter',chapter.url+'.xml'))

    # saving sequentials xmls inside 'sequential' folder
    # saving vertical xmls inside 'vertical' folder
    for chapter in data.chapters:
        for sequential in chapter.sequentials:
            sequential_xml = Element('sequential')
            sequential_xml.attrib['display_name'] = sequential.name

            if chapter.url != 'sec_00':
                if sequential.name == 'Assignments':
                    sequential_xml.attrib['format'] = "Research"
                else:
                    sequential_xml.attrib['format'] = "Self-check"

                sequential_xml.attrib['graded'] = "true"

            #getting units
            units = split_into_units(sequential.source_notebook)

            for i, unit in enumerate(units):
                vertical_url = sequential.url + '_{0}'.format(str(i).zfill(2))
                # add vertical info to sequential_xml
                vertical_sub = SubElement(sequential_xml, 'vertical')
                vertical_sub.attrib['url_name'] = vertical_url

                # creating vertical.xml
                vertical_xml = Element('vertical')
                vertical_xml.attrib['display_name'] = unit.metadata.name


                unit_output = convert_unit(unit, date=sequential.date)
                for (j,out) in enumerate(unit_output):
                    out_url = vertical_url + "_out_{0}".format(str(j).zfill(2))
                    if out[0] == 'html':
                        # adding html subelement
                        html_subelement = SubElement(vertical_xml, 'html')
                        html_subelement.attrib['url_name'] = out_url

                        # creating html xml
                        html_xml = Element('html')
                        html_xml.attrib['display_name'] = unit.metadata.name
                        html_xml.attrib['filename'] = out_url

                        save_xml(html_xml, os.path.join(dirpath,'html',
                                                        out_url+'.xml'))

                        body = out[1]
                        body = body.replace('src="figures/',
                                            'src="/static/'+chapter.url+'_')

                        html_path = os.path.join(dirpath,'html',
                                                 out_url+'.html')
                        save_html(body, html_path)

                    elif out[0] == 'MoocVideo':
                        # adding video subelement
                        video_subelement = SubElement(vertical_xml, 'video')
                        video_subelement.attrib['url_name'] = out_url

                        # creating video xml
                        video_xml = out[1]
                        video_path = os.path.join(dirpath, 'video',
                                                  out_url + '.xml')
                        save_xml(video_xml, video_path)

                    elif out[0] == 'MoocDiscussion':
                        # adding video subelement
                        discussion_xml = out[1]

                        discussion_subelement = SubElement(vertical_xml,
                                                           'discussion')
                        discussion_subelement.attrib['url_name'] = \
                                discussion_xml.attrib['discussion_id']

                        # creating video xml
                        discussion_path = os.path.join(dirpath, 'discussion',
                                                       out[2]+'.xml')
                        save_xml(discussion_xml, discussion_path)

                    elif out[0] == 'MoocPeerAssessment':
                        peer_sub = out[1]
                        if 'url_name' not in peer_sub.attrib.keys():
                            peer_sub.attrib['url_name'] = out_url+'_'+'peer'
                        vertical_xml.append(peer_sub)

                    elif out[0] == 'MoocSelfAssessment':
                        self_sub = out[1]
                        if 'url_name' not in self_sub.attrib.keys():
                            self_sub.attrib['url_name'] = out_url+'_'+'self'
                        vertical_xml.append(self_sub)

                    elif out[0] in ('MoocCheckboxesAssessment',
                                    'MoocMultipleChoiceAssessment'):
                        # adding problem subelement
                        problem = SubElement(vertical_xml, 'problem')
                        problem.attrib['url_name'] = out_url

                        # creating problem xml
                        problem_xml = out[1]
                        problem_path = os.path.join(dirpath, 'problem',
                                                    out_url+'.xml')

                        save_xml(problem_xml, problem_path)

                save_xml(vertical_xml, os.path.join(dirpath, 'vertical',
                                                    vertical_url+'.xml'))
            save_xml(sequential_xml, os.path.join(dirpath, 'sequential',
                                                  sequential.url+'.xml'))

    # copying figures
    for chapter in data.chapters:
        figures_list = []
        for sequential in chapter.sequentials:
            fig_path = os.path.join(content_folder,
                                    os.path.dirname(sequential.source_notebook),
                                    'figures')
            if os.path.exists(fig_path):
                files = os.listdir(fig_path)
                for f in files:
                    if f not in figures_list:
                        figures_list.append(fig_path + '/' + f)

        for f in figures_list:
            destination = os.path.join(dirpath, 'static', chapter.url + '_' +
                                       f.split('/')[-1])
            shutil.copy(f, destination)

    # Creating tar
    target = mooc_folder + '/generated'
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    tar_filepath = target + '/import_to_edx.tar.gz'
    tar = tarfile.open(name=tar_filepath, mode='w:gz')
    tar.add(dirpath, arcname='')
    tar.close()

    # Some debugging
    if args.debug:
        shutil.copytree(dirpath, target + '/files')
    if args.open:
        if not args.debug:
            print('--open flag works only with debug')
        else:
            subprocess.check_call(['nautilus', '--', target + '/files'])

    # Cleaning
    shutil.rmtree(dirpath)


def warn_about_status(mooc_folder):
    git = 'git --git-dir={0}/.git --work-tree={0}/ '.format(mooc_folder)
    status = subprocess.check_output(git + "status", shell=True).split("\n")[0]
    if "On branch master" not in status:
        print("Not on master branch, do not upload to edx.\n",
              "Press Enter to continue.")
        raw_input()
        return
    if subprocess.check_output(git + "diff", shell=True):
        print("Some files are modified, do not upload to edx.\n",
              "Press Enter to continue.")
        raw_input()

def main():
    mooc_folder = os.path.join(os.path.dirname(__file__), os.path.pardir)
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug', action='store_true',
                        help='debugging flag')
    parser.add_argument('-o', '--open', action='store_true',
                        help='opening uncompressed folder with files')

    args = parser.parse_args()

    if args.debug:
        msg = 'Debug mode : folder %s will contain uncompressed data.'
        print(msg % (mooc_folder + '/generated/files'))

    print('Path to mooc folder:', mooc_folder)
    warn_about_status(mooc_folder)
    converter(mooc_folder, args)

if __name__ == "__main__":
    main()

