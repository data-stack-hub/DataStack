import importlib.util as imputil
import importlib, sys, inspect, os, json


def _module_to_namespace(namespace):
    # if isinstance(namespace, ModuleType):
        members = inspect.getmembers(
            namespace, lambda o: inspect.isfunction(o) or isinstance(o, type)
        )
        return {key: mod for key, mod in members}

def code_to_fn(function_name, code=''):
    spec = imputil.spec_from_loader('my_module', loader=None)
    my_module = importlib.util.module_from_spec(spec)
    exec(code, my_module.__dict__)
    sys.modules['my_module'] = my_module
    # print(my_module.__dict__)
    namespace  = _module_to_namespace(my_module)
    if function_name in namespace:
        fn = namespace[function_name]
        # print(fn)
        params = {}
        return fn(**params)
    else:
        # print('function not found')
        return {'error':'not found'}

def run_fn_by_name(function_name):
    # print({k: v for k, v in globals().items() if not k.startswith("__")})
    pass

def read_notebook(path):
    import codecs
    import json, os
    from urllib.parse import urlparse
    notebook_name = path
    ROOT_DIR = os.path.abspath('')
    # data_path = os.path.join(ROOT_DIR, r'data\notebooks')
    result = urlparse(path)
    if not result.netloc:
        path = os.path.join(ROOT_DIR , notebook_name)
    f = codecs.open(path, 'r')
    source = f.read()

    y = json.loads(source)
    pySource = '##Python .py code from .jpynb:\n'
    for x in y['cells']:
        if x['cell_type'] == 'code':
            for x2 in x['source']:
                pySource = pySource + x2
                if x2[-1] != '\n':
                    pySource = pySource + '\n'
    return pySource

def code_to_module(code, module_name = 'mymodule'):
    # print('code_to_module', module_name)
    import sys, imp
    mymodule = imp.new_module(code)
    # exec(code, mymodule.__dict__)
    sys.modules[module_name] = mymodule
    globals()[module_name] = mymodule
    # print(module_name, globals()[module_name])
    return mymodule