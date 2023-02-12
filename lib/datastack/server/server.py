from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from utils import *
app = Flask(__name__)
cors = CORS(app)

# params get - request.args.to_dict()
# params post - request.json
routes = [
        {'path':'/', 'fn':'load_app'},
        {'path':'/run_fn','fn':'run_fn'},
        {'path':'/editable', 'fn':'save_editable'}
    ]
my_module = importlib.import_module('test_app')
mymodule_global_vars = [{k: v} for k, v in my_module.__dict__.items() if not k.startswith("__")]
def load_app():
    """
    get datastack class from the module
    """
    print(my_module.__dict__)
    cls = getattr(my_module, 'ds')
    return jsonify(cls.build_app())

def rerun():
    # get_scheduler_status()
    global a1
    a1 = {k: v for k, v in my_module.__dict__.items() if not k.startswith("__")}
    return jsonify(getattr(my_module, 'ds').rerun(a1, {}))

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

if __name__ == '__main__':
  app.run(debug=True)
