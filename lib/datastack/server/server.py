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

def update_block(app_json, block, parent):
    block_status = False
    def it(e):
        nonlocal block_status
        for it_block in e:
            print('it_block', it_block)
            if it_block['_id']== block['_id']:
                print('block found')
                it_block.update(block)
                block_status = True
                break
            if 'type' in it_block and it_block['type'] == 'expander':
                it(it_block['prop']['html'])
    it(app_json)
    print(block_status, app_json)
    if not block_status:
        # par = [p_block for p_block in app_json if p_block['_id'] == parent['_id']]
        try:
            for p_block in app_json:
                if p_block['_id'] == parent['_id']:
                    print('parent found', p_block)
                    p_block['prop']['html'].append(block)
        except:
            app_json.append(block)
    return app_json

def save_editable():
    import json
    logger.info('saving editable %s', request.json)

    dump = {
        'id':request.json['wid'],
        'block':request.json
    }
    if request.json['type'] == "editable_html":
        print(request.json)
        # update all bloacked from payload
        # b = [request.json['payload'] if block['_id'] == request.json['payload']['_id'] else block for block in dump['block']['prop']['html'] ]
        # dump['block']['prop']['html'] = b
        # # check for new block
        # c = [block  for block in dump['block']['prop']['html'] if block['_id'] == request.json['payload']['_id'] ]
        # print('c',c)
        # if not c:
        #     dump['block']['prop']['html'].append(request.json['payload'])
    with open('app.json', 'r') as f:
        try:
            app_json = json.loads(f.read())
        except:
            app_json = {request.json['wid'] : dump}
        app_json[request.json['wid']]['block']['prop']['html'] = update_block(app_json[request.json['wid']]['block']['prop']['html'],request.json['payload']['block'], request.json['payload']['parent'])
        # app_json[request.json['wid']] = dump
    with open('app.json', 'w') as f:
        f.write(json.dumps(app_json))
    return {'True':"true"}

def run_block():

    from io import StringIO
    from contextlib import redirect_stdout
    import json
    f = StringIO()
    with redirect_stdout(f):
        # exec(request.json['prop']['code'])
        # run each lins as seprate node
        exec(request.json['prop']['code'], my_module.__dict__)
    s = f.getvalue()

    import ast, pandas
    tree = ast.parse(request.json['prop']['code'], 'script_path', "exec")
    body = getattr(tree, "body")
    last_node = body[-1]
    print(s.split())
    for es in s.split():
        print(ast.literal_eval(es))
    # print(type(ast.literal_eval(s)))
    if type(last_node) is ast.Expr:
        if 'id' in last_node.__dict__['value'].__dict__:
            id = last_node.__dict__['value'].__dict__['id']
            last_node_value = getattr(my_module, id)
            print(type(last_node_value))
            if isinstance(last_node_value, pandas.DataFrame):
                s= last_node_value.head(20).to_html()
                return {'res':s,"type":'table'}
            try:
                if last_node_value.__module__ == "plotly.graph_objs._figure":
                    import base64
                    img_bytes = last_node_value.to_image(format="jpeg")
                    img_string = base64.b64encode(img_bytes).decode('utf-8')
                    return {'res':img_string, "type":'image'}
                    # return {'res':last_node_value.to_html(full_html =False, include_plotlyjs ='cdn'), "type":'table'}

            except:
                logger.error('error while checking plotly class')
    # with open('app.json', 'r') as f:
    #     try:
    #         app_json = json.loads(f.read())
    #     except:
    #         app_json = {}
    #     app_json[request.json['wid']]['block']['prop']['last_run_result'] = s
    # with open('app.json', 'w') as f:
    #     f.write(json.dumps(app_json))

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
