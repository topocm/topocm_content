import sys
import os
import secrets
from textwrap import dedent

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree

from hashlib import md5

from IPython import display
import feedparser

module_dir = os.path.dirname(__file__)
sys.path.extend(module_dir)


__all__ = [
    'MoocVideo', 'PreprintReference', 'MoocDiscussion',
    'MoocCheckboxesAssessment', 'MoocMultipleChoiceAssessment',
    'MoocSelfAssessment'
]


def _add_solution(el, text):
    """Add a solution xml to a problem."""
    sol = SubElement(el, 'solution')
    div = SubElement(sol, 'div')
    div.attrib['class'] = 'detailed-solution'
    title = SubElement(div, 'p')
    title.text = 'Explanation'
    content = SubElement(div, 'p')
    content.text = text


class MoocComponent:
    def _repr_mimebundle_(self, include, exclude):
        return {
            'application/vnd.edx.olxml+xml':
            ElementTree.tostring(self.xml, encoding='unicode'),
        }


class MoocVideo(MoocComponent, display.YouTubeVideo):
    def __init__(self, id, src_location=None, res='720', display_name="",
                 download_track='true', download_video='true',
                 show_captions='true', **kwargs):
        """A video component of an EdX mooc embeddable in IPython notebook."""

        self.xml = Element('video', attrib=dict(
            youtube=f'1.00:{id}',
            youtube_id_1_0=id,
            display_name=display_name,
            download_track=download_track,
            download_video=download_video,
            show_captions=show_captions,
            **kwargs,
        ))

        if src_location is not None:
            self.xml.attrib['source'] = (
                "http://delftxdownloads.tudelft.nl/TOPOCMx-QuantumKnots/"
                f"TOPOCMx-{src_location}-video.{res}.mp4"
            )

        super().__init__(id, rel=0, cc_load_policy=1)

    def _repr_html_(self):
        orig = super()._repr_html_()
        return (
            '<div class="embed-responsive embed-responsive-16by9">{}</div>'
            .format(orig.replace(
                '<iframe',
                '<iframe class="embed-responsive-item" '
            ))
        )


class PreprintReference:
    def __init__(self, index, description="", show_abstract=True):
        """Formatted basic information from arxiv preprint."""

        arxiv_query = "http://export.arxiv.org/api/query?id_list="
        self.index = index
        self.show_abstract = show_abstract
        self.description = description
        self.data = feedparser.parse(arxiv_query + index)

    def _repr_html_(self):
        data = self.data
        ind = self.index
        title = data['entries'][0]['title']
        s = '<h3 class="title mathjax">' + title + '</h3>'

        s += f'<p><a href=http://arxiv.org/abs/%s>http://arxiv.org/abs/%s</a><br>' % (ind, ind)

        s += '<div class="authors">'
        s += ", ".join(author.name for author in data['entries'][0]['authors'])
        s += '</div></p>'

        if self.show_abstract:
            s += '<p><blockquote class="abstract mathjax">'
            s += data['entries'][0]['summary']
            s += '</blockquote></p>'

        if self.description:
            s += '<p><b>Hint:</b> %s </p>' % self.description

        return s


class MoocSelfAssessment(MoocComponent):
    def __init__(self):
        self.placeholder = (
            '<p><b> MoocSelfAssessment description</b></p>\n'
            '<p><b>In the live version of the course, you would '
            'need to share your solution and grade yourself.'
            '</b></p>'
        )

        content_filename = module_dir + '/xmls/openassessment_self.xml'
        with open(content_filename, 'r') as content_file:
            self.xml = xml = ElementTree.fromstring(content_file.read())

        assessment = xml.find('assessments').find('assessment')

        xml.attrib['submission_start'] = '2001-12-31T10:00:00Z'
        xml.attrib['submission_due'] = '2100-12-31T10:00:00Z'

        assessment.attrib['start'] = '2001-12-31T10:00:00Z'
        assessment.attrib['due'] = '2100-12-31T10:00:00Z'

    def _repr_html_(self):
        return self.placeholder


class MoocCheckboxesAssessment(MoocComponent):
    def __init__(self, question, answers, correct_answers, max_attempts=2,
                 display_name="Question", explanation=None):
        """
        MoocCheckboxesAssessment component

        input types
        -----------

        question : string
        answers : list of strings
        correct_answers : list of int

        """
        self.xml = xml = Element('problem', attrib=dict(
            display_name=display_name,
            max_attempts=str(max_attempts),
        ))

        SubElement(xml, 'p', text='question')
        SubElement(xml, 'p', text='Select the answers that match')

        sub = SubElement(xml, 'choiceresponse')
        sub = SubElement(sub, 'checkboxgroup')
        sub.attrib['label'] = "Select the answers that match"
        sub.attrib['direction'] = "vertical"

        for i, ans in enumerate(answers):
            choice = SubElement(sub, 'choice')
            if i in correct_answers:
                choice.attrib['correct'] = 'true'
            else:
                choice.attrib['correct'] = 'false'
            choice.text = ans

        if explanation is not None:
            _add_solution(xml, explanation)

        self.question = question
        self.answers = answers
        self.correct_answers = correct_answers
        self.explanation = explanation

    def _repr_html_(self):
        s = '<h4>%s</h4>' % self.question
        s += '<form><input type="checkbox">  '
        s += '<br><input type="checkbox">  '.join(self.answers)
        s += '</form>'

        answer = 'The correct answer{0}:<br>'.format(
            's are' if len(self.correct_answers) > 1 else ' is'
        )
        tmp = []
        for i in self.correct_answers:
            tmp.append(self.answers[i])
        answer += ', '.join(t for t in tmp)
        answer += '.'
        if self.explanation is not None:
            answer += '<br><i>' + self.explanation + '</i>'

        s += dedent("""
        <button title="Click to show/hide content" type="button"
        onclick="if(document.getElementById('{0}')
         .style.display=='none') {{document.getElementById('{0}')
         .style.display=''}}else{{document.getElementById('{0}')
         .style.display='none'}}">Show answer</button>

        <div id="{0}" style="display:none">
        {1} <br>
        </div>    """)
        return s.format(secrets.token_urlsafe(20), answer)


class MoocMultipleChoiceAssessment(MoocComponent):
    def __init__(self, question, answers, correct_answer, max_attempts=2,
                 display_name="Question", explanation=None):
        """
        MoocMultipleChoiceAssessment component

        Parameters:
        -----------

        question : string
        answers : list of strings
        correct_answers : int

        """
        self.xml = xml = Element('problem', attrib=dict(
            display_name=display_name,
            max_attempts=str(max_attempts),
        ))

        SubElement(xml, 'p', text=question)
        SubElement(xml, 'p', text='Please select correct answer')

        sub = SubElement(xml, 'multiplechoiceresponse')
        sub = SubElement(sub, 'choicegroup')
        sub.attrib['label'] = "Please select correct answer"
        sub.attrib['type'] = "MultipleChoice"

        for i, ans in enumerate(answers):
            choice = SubElement(sub, 'choice')
            if i == correct_answer:
                choice.attrib['correct'] = 'true'
            else:
                choice.attrib['correct'] = 'false'
            choice.text = ans

        if explanation is not None:
            _add_solution(xml, explanation)

        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.explanation = explanation

    def _repr_html_(self):
        s = '<h4>%s</h4>' % self.question
        s += '<form>'
        for ans in self.answers:
            s += f'<input type="radio" name="answer" value="{ans}">{ans}<br>'
        s += '</form>'

        answer = 'The correct answer is: <br>'
        answer += self.answers[self.correct_answer]
        if self.explanation is not None:
            answer += f'<br><i>' + self.explanation + '</i>'

        s += dedent("""
        <button title="Click to show/hide content" type="button"
        onclick="if(document.getElementById('{0}')
         .style.display=='none') {{document.getElementById('{0}')
         .style.display=''}}else{{document.getElementById('{0}')
         .style.display='none'}}">Show answer</button>

        <div id="{0}" style="display:none">{1}</div>""")
        return s.format(secrets.token_urlsafe(20), answer)


class MoocDiscussion(MoocComponent):
    def __init__(
        self, discussion_category, discussion_target, display_name=None,
        discussion_id=None, **kwargs,
    ):
        discussion_id = md5(
            discussion_category.encode('utf-8')
            + discussion_target.encode('utf-8')
        ).hexdigest()
        self.xml = Element('discussion', attrib=dict(
            discussion_category=discussion_category,
            discussion_target=discussion_target,
            display_name=(display_name or discussion_target),
            discussion_id=discussion_id,
            url_name=discussion_id,
            **kwargs
        ))
        self.display_name = (display_name or discussion_target)

    def _repr_html_(self):
        return (
            f"<p><b>Discussion</b> {self.display_name}"
            " is available in the EdX version of the course.</p>"
        )
