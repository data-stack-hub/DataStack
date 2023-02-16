from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

from datastack.runtime import runtime
from datastack.logger import logger

app = Flask(__name__)
cors = CORS(app)

# params get - request.args.to_dict()
# params post - request.json
routes = [
        {'path':'/', 'fn':'load_app'},
        {'path':'/run_fn','fn':'run_fn'},
        {'path':'/editable', 'fn':'save_editable'},
        {'path':'/run_block', 'fn':'run_block'},
        {'path':'/run_query_block', 'fn':'run_query_block'}
    ]


def load_app():
    """
    get datastack class from the module
    """
    params = request.args.to_dict()
    if not params['session_id']:
        runtime.create_session()
    else:
        logger.info('seeesion_id: %s', params['session_id'])
    return jsonify(runtime.get_main_class().build_app())

def rerun():
    global a1
    a1 = {k: v for k, v in my_module.__dict__.items() if not k.startswith("__")}
    return jsonify(runtime.get_main_class().rerun(a1, {}))

def save_editable():
    logger.info('saving editable %s', request.json['payload'])
    with open(request.json['prop']['name']+'.txt',"w")  as file:
        file.write(request.json['payload'])
    return {'True':"true"}

def run_block():

    from io import StringIO
    from contextlib import redirect_stdout

    f = StringIO()
    with redirect_stdout(f):
        # exec(request.json['prop']['code'])
        exec(request.json['prop']['code'], my_module.__dict__)
    s = f.getvalue()
    print(s)
    return {'res':s}

def run_query_block():
    query = request.json['prop']['query']
    import sqlite3
    import pandas as pd
    cnx = sqlite3.connect('file.db')
    print(runtime.get_main_class().__dict__)
    return {'res':pd.read_sql(query,cnx).to_html()}

def update_var(aaa):
    setattr(my_module,aaa['prop']['input_var'], aaa['payload'])

def update_var_select(aaa):
    setattr(my_module, aaa['prop']['value_frm'], aaa['payload'])
    getattr(my_module,aaa['prop']['on_change_name'])()

def run_fn():
    global my_module 
    my_module = runtime.get_module()
    if request.json['prop']['on_click_name'] == 'update_var':
        update_var(request.json)
    elif request.json['prop']['on_click_name'] == 'update_var_select':
        update_var_select(request.json)
    else:
        fn = getattr(my_module, request.json['prop']['on_click_name'])
        fn(request.json)
    return rerun()

def fn(method_name):
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    return method

for route in routes:
    app.add_url_rule(route['path'], view_func=fn(route['fn']), methods = ["get","post"])

def start_server(file_path):
    global my_module
    runtime.set_file_path(file_path)
    runtime.run_script(file_path)
    my_module = runtime.get_module()

    logger.debug("Starting server...")
    app.run(debug=True)
    logger.debug("Server started on port 5000")
if __name__ == '__main__':
    start_server()
