import importlib, os
from datastack.server import utils
from datastack.logger import logger
ctx = {}

ctx['storage'] = []
def set_main_class(cls):
    ctx['main_class'] = cls

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

def get_shell():
    return ctx['shell']

from IPython.core.interactiveshell import InteractiveShell
ctx['shell'] = InteractiveShell().get_ipython()

def run_code_shell(code):
    from io import StringIO
    from contextlib import redirect_stdout
    import json
    f = StringIO()
    with redirect_stdout(f):
        ctx['shell'].run_cell(code, shell_futures = True)
    s = f.getvalue()
    print(s, ctx['shell'].last_execution_result)
    print(ctx['shell'].payload_manager.read_payload())
    return s


from jupyter_client import KernelManager
km = KernelManager()
km.start_kernel()
kc = km.client()
def run_code(code):

    # now execute something in the client
    kc.execute("""
    2+2
    print(5+5)

    """)
    kc_msg=''
    while True:
        try:
            kc_msg = kc.get_iopub_msg(timeout=1)
            if 'content' in kc_msg and 'data' in kc_msg['content']:
                print('the kernel produced data {}'.format(kc_msg['content']))
                break        
        except Exception as e:
            print('timeout kc.get_iopub_msg',e)
            pass

    return kc_msg

    
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
    # from io import StringIO
    # from contextlib import redirect_stdout
    # f = StringIO()
    # with redirect_stdout(f):
    exec(code, my_module.__dict__)
    # get_main_class().write(f.getvalue())
    update_module(my_module)

def create_session():
    """
    check if session is available with session id
    create session if not available - class
    id,script data, state, script runner, user info, session state
    """
    reset_main_class()
    run_script(get_file_path())
    return 'session_id'    