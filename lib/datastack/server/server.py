from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from datastack.server import utils
from datastack.runtime import runtime
import importlib, os
app = Flask(__name__)
cors = CORS(app)

# params get - request.args.to_dict()
# params post - request.json
routes = [
        {'path':'/', 'fn':'load_app'},
        {'path':'/run_fn','fn':'run_fn'},
        {'path':'/editable', 'fn':'save_editable'}
    ]

# print(utils.read_notebook("test_app.ipynb"))
# my_module = utils.code_to_module(utils.read_notebook('test_app.ipynb'))
# print('module',my_module)

file_name = 'test_app.ipynb'
if os.path.splitext(file_name)[1] == '.ipynb':
    filebody = utils.read_notebook(file_name)
else:
    with open(file_name) as f:
        filebody = f.read()

# print(filebody)
try:
    code = compile(filebody,filename=file_name, mode="exec",flags=0,dont_inherit=1,optimize=-1)
    print(code)
except Exception as e:
    print(e)
spec = importlib.util.spec_from_loader('my_module', loader=None)
my_module = importlib.util.module_from_spec(spec)
exec(code, my_module.__dict__)
# my_module = importlib.import_module('test_app')
print('module1', my_module)
# mymodule_global_vars = [{k: v} for k, v in my_module.__dict__.items() if not k.startswith("__")]
def load_app():
    """
    get datastack class from the module
    """
    # print(my_module.__dict__)
    # cls = getattr(my_module, 'ds')
    print(runtime.get_main_class().__dict__)
    return jsonify(runtime.get_main_class().build_app())

def rerun():
    # get_scheduler_status()
    global a1
    a1 = {k: v for k, v in my_module.__dict__.items() if not k.startswith("__")}
    return jsonify(runtime.get_main_class().rerun(a1, {}))

def save_editable():
    print('saving editable', request.json['payload'])
    with open(request.json['prop']['name']+'.txt',"w")  as file:
        file.write(request.json['payload'])
    return {'True':"true"}


def update_var(aaa):
    setattr(my_module,aaa['prop']['input_var'], aaa['payload'])
    # globals()[f"input_value"]=aaa['payload']
    # globals()[aaa['prop']['input_var']]=aaa['payload']
    # print(globals()[f"input_var"], aaa['payload'])

def update_var_select(aaa):
    setattr(my_module, aaa['prop']['value_frm'], aaa['payload'])
    # globals()[aaa['prop']['value_frm']]=aaa['payload']
    getattr(my_module,aaa['prop']['on_change_name'])()
    # globals()[aaa['prop']['on_change_name']]()

def run_fn():
    if request.json['prop']['on_click_name'] == 'update_var':
        update_var(request.json)
    elif request.json['prop']['on_click_name'] == 'update_var_select':
        update_var_select(request.json)
    else:
        fn = getattr(my_module, request.json['prop']['on_click_name'])
        fn(request.json)
    return rerun()

def fn(method_name):
    print(method_name)
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    return method

for route in routes:
    app.add_url_rule(route['path'], view_func=fn(route['fn']), methods = ["get","post"])

def start_server():
    app.run(debug=True)
if __name__ == '__main__':
  app.run(debug=True)
