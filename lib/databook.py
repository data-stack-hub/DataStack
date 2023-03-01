import datastack as ds
from datastack.server import utils
import importlib, os


# # imports
# import sys
# sys.path.append(r'\\fs02\Engineering\IndiaTeam\Projects\vvora\sm')
# from data_stack import sql, datasets, report, email_smtp, chart
# from enovix_sm import fn

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
# import bamboolib as bam

# config
pd.set_option("display.precision", 3)

# def run_notebook(a):
print('getting notebook...')
path = r"\\fs02\Engineering\IndiaTeam\Projects\vvora\sm\data\notebooks\pilot_yield_ds.ipynb"
local_path = r'C:\Users\vvora\Desktop\vishal_vora\projects\datastack\data\notebooks\Untitled9.ipynb'
filebody = utils.read_notebook(path)

code = compile(filebody,filename=path, mode="exec",flags=0,dont_inherit=1,optimize=-1)
spec = importlib.util.spec_from_loader('my_module', loader=None)
my_module = importlib.util.module_from_spec(spec)
exec(code)


# ds.button('run notebook', on_click=run_notebook)
ds.editable_html('databook1')
exec("a=10")


