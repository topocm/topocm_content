##Short description of the Ipython 3 to/from Python converter files.

The *ipython notebook --script* run option that produced python codes
from an Ipython 2 notebook is deprecated in Ipython 3 (Jupyter, nbformat 4).
The python file that Jupyter can produce has several shortcomings, the most
problematic one is the missing metainformation: there is no cell type
metadata, just a bracket indicates where a new code cell starts, but information
about markdowncells are completly lost. This is why restoring the
notebook (without the output content) without losing important
information is not possible right now.


The scripts in the folder suggest a solution to this problem.

+ *notebook_v4_to_py.py* converts an Ipython notebook to py file that preserves
cell metadata. The conversion can be done manually by running the following
command

python notebook_v4_to_py.py -f notebook_filename.ipynb

+ While this script works, it is much more convenient to make Jupyter create
the python file itself automatically. This can be done by adding the content
of *ipython_notebook_config.txt* to the ipython_notebook_config.py in the config
file which can be located with

ipython locate profile default

+ The python files then can be version controlled, and the converter script that
creates a notebook feom the .py file is *py_to_notebook_v4.py*:

python py_to_notebook_v4.py -f py_filename.py

Call the scripts with argument "--overwrite" to overwrite existing .ipynb or
.py files.

Call the scripts with argument "--dry-run" to simulate (print out) what would
happen.