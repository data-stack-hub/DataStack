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
        print(fn)
        params = {}
        return fn(**params)
    else:
        print('function not found')
        return {'error':'not found'}

def run_fn_by_name(function_name):
    print({k: v for k, v in globals().items() if not k.startswith("__")})