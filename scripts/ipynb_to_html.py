import os
import glob
import subprocess
html_dir = '../generated/html/'
ipynbs = glob.glob("../**/*.ipynb", recursive=True)
figures = glob.glob("../**/figures/*", recursive=True)

cmd = "jupyter nbconvert --to html --config links_config.py --template=template.tpl {}"

for ipynb in ipynbs:
    path, fname = os.path.split(ipynb.replace(".ipynb", ".html"))
    html_loc = path + "/" + fname
    html_loc_new = html_dir + html_loc[3:]
    os.makedirs(html_dir + path[3:], exist_ok=True)
    subprocess.call(cmd.format(ipynb).split(" "))
    subprocess.call("mv {} {}".format(html_loc, html_loc_new).split(" "))

for figure in figures:
    path, fname = os.path.split(figure)
    os.makedirs(html_dir + path[3:], exist_ok=True)
    subprocess.call("cp {} {}".format(figure, html_dir + figure[3:]).split(" "))