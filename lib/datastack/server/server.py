from flask import Flask
from flask import request
from flask_cors import CORS
# from  test_app import *
# import ex_test
from utils import *
app = Flask(__name__)
cors = CORS(app)

# params get - request.args.to_dict()
# params post - request.json
routes = [
        {'path':'/', 'fn':'load_app'},
        {'path':'/run_fn','fn':'run_fn'}
    ]
my_module = importlib.import_module('test_app')
def load_app():
    fn = getattr(my_module, 'test')
    return fn()

def run_fn():
    # print(request.json)
    fn = getattr(my_module, request.json['prop']['on_click_name'])
    fn(request.json)
    # print(ex.__dict__)
    return getattr(my_module, 'rerun')()

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
