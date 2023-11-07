import importlib, os
from datastack.server import utils
from datastack.logger import logger
ctx = {}

ctx['storage'] = []
def set_main_class(cls):
    ctx['main_class'] = cls

def collect_cls(cls):
    ctx['storage'].append(cls)

def return_collect_cls():
    return ctx['storage']

def get_main_class():
    return ctx['main_class']

def reset_main_class():
    ctx['main_class'].dump_app()
    
def update_module(module):
    ctx['module'] = module

def get_module():
    return ctx['module']

def set_file_path(path):
    ctx['file_path'] = path

def get_file_path():
    return ctx['file_path']

def add_file_to_storage(file):
    ctx['storage'].append(file)

def run_script(path):
    logger.info('Script run init')
    if os.path.splitext(path)[1] == '.ipynb':
        filebody = utils.read_notebook(path)
    else:
        with open(path) as f:
            filebody = f.read()

    try:
        code = compile(filebody,filename=path, mode="exec",flags=0,dont_inherit=1,optimize=-1)
    except Exception as e:
        logger.error('script failed with error: %s',e)
    spec = importlib.util.spec_from_loader('my_module', loader=None)
    my_module = importlib.util.module_from_spec(spec)
    from pathlib import Path
    script_path = os.path.abspath(path)
    script_folder = os.path.dirname(script_path)
    import sys
    sys.path.insert(0,os.path.dirname(script_path))
    from io import StringIO
    from contextlib import redirect_stdout
    f = StringIO()
    exec(code, my_module.__dict__)
    # with redirect_stdout(f):
    
    #     exec("""print(df.col1)""", my_module.__dict__)
    print(f.getvalue())
    # get_main_class().write(f.getvalue())
    import pandas as pd
    import inspect
    # print(inspect.getmembers(my_module))
    update_module(my_module)
    ctx['main_class'].get_all_dfs()


def create_session():
    """
    check if session is available with session id
    create session if not available - class
    id,script data, state, script runner, user info, session state
    """
    # reset_main_class()
    # run_script(get_file_path())
    return 'session_id'