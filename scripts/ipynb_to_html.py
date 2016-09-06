import os
import glob
import subprocess
html_dir = 'generated/html/'
ipynbs = glob.glob("**/*.ipynb", recursive=True)
figures = glob.glob("**/figures/*", recursive=True)

cmd = "jupyter nbconvert --to html --config scripts/website_config.py --template=scripts/website_template.tpl {}"

for ipynb in ipynbs:
    path, fname = os.path.split(ipynb.replace(".ipynb", ".html"))
    html_loc = path + ("/" if path else "") + fname
    html_loc_new = html_dir + html_loc
    os.makedirs(html_dir + path, exist_ok=True)
    subprocess.call(cmd.format(ipynb).split(" "))
    subprocess.call("mv {} {}".format(html_loc, html_loc_new).split(" "))

for figure in figures:
    path, fname = os.path.split(figure)
    os.makedirs(html_dir + path, exist_ok=True)
    subprocess.call("cp {} {}".format(figure, html_dir + figure).split(" "))
