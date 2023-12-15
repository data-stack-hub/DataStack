from typing import overload
from flask import Flask
from flask import request, jsonify, send_from_directory
from flask_cors import CORS
from waitress import serve
from datastack.runtime import runtime
from datastack.runtime import session_manager
from datastack.logger import logger
import os
import json
import numpy as np
from pathlib import Path

static_file_path = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute(), "static"
)
app = Flask(
    __name__,
    static_folder=static_file_path,
    template_folder=static_file_path,
    static_url_path="/",
)
cors = CORS(app)

seesion_mgr = session_manager.SessionManager()
routes = [
    {"path": "/", "fn": "get_app"},
    {"path": "/app", "fn": "load_app"},
    {"path": "/run_fn", "fn": "run_fn"},
    {"path": "/editable", "fn": "save_editable"},
    {"path": "/run_block", "fn": "run_block"},
    {"path": "/run_query_block", "fn": "run_query_block"},
    {"path": "/get_df_column", "fn": "get_df_column"},
    {"path": "/ds_active_sessions", "fn": "get_active_sessions"},
]


def get_app():
    return send_from_directory(static_file_path, "index.html")


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def load_app():
    """
    get datastack class from the module
    """
    params = request.args.to_dict()

    session = seesion_mgr.connect_session()
    print(seesion_mgr.__dict__)
    return json.dumps(session.main_class.build_app(), cls=NpEncoder)


def rerun(cls, my_module, session):
    global a1
    a1 = {k: v for k, v in my_module.__dict__.items() if not k.startswith("__")}
    # my_module.cls = cls
    # class_name = session.class_object_name
    # print('class_name',class_name)
    print(session.main_class.rerun(a1))
    return json.dumps(session.main_class.rerun(a1), cls=NpEncoder)


def get_active_sessions():
    for key, value in seesion_mgr.session().items():
        print(key, value["session"].__dict__)
    return [
        session["session"].__dict__["user"]
        for key, session in seesion_mgr.session().items()
    ]


def update_block(app_json, block, parent):
    block_status = False

    def it(e):
        nonlocal block_status
        for it_block in e:
            print("it_block", it_block)
            if it_block["_id"] == block["_id"]:
                print("block found")
                it_block.update(block)
                block_status = True
                break
            if "type" in it_block and it_block["type"] == "expander":
                it(it_block["prop"]["html"])

    it(app_json)
    print(block_status, app_json)
    if not block_status:
        # par = [p_block for p_block in app_json if p_block['_id'] == parent['_id']]
        if parent["is_root"]:
            print(parent)
            app_json.append(block)
        else:
            try:
                for p_block in app_json:
                    if p_block["_id"] == parent["_id"]:
                        print("parent found", p_block)
                        p_block["prop"]["html"].append(block)
            except:
                app_json.append(block)
    return app_json


def save_editable():
    import json

    logger.info("saving editable %s", request.json)

    dump = {"id": request.json["wid"], "block": request.json}
    if request.json["type"] == "editable_html":
        print(request.json)
        # update all bloacked from payload
        # b = [request.json['payload'] if block['_id'] == request.json['payload']['_id'] else block for block in dump['block']['prop']['html'] ]
        # dump['block']['prop']['html'] = b
        # # check for new block
        # c = [block  for block in dump['block']['prop']['html'] if block['_id'] == request.json['payload']['_id'] ]
        # print('c',c)
        # if not c:
        #     dump['block']['prop']['html'].append(request.json['payload'])

    file_path = os.path.join(
        Path(os.path.dirname(__file__)).parent.absolute(), "static/app.json"
    )
    try:
        with open(file_path, "r") as f:
            app_json = json.loads(f.read())
    except:
        app_json = {request.json["wid"]: dump}
    app_json[request.json["wid"]]["block"]["prop"]["html"] = update_block(
        app_json[request.json["wid"]]["block"]["prop"]["html"],
        request.json["payload"]["block"],
        request.json["payload"]["parent"],
    )
    # app_json[request.json['wid']] = dump
    with open(file_path, "w") as f:
        f.write(json.dumps(app_json))
    return {"True": "true"}


def run_block():

    from io import StringIO
    from contextlib import redirect_stdout
    import json

    f = StringIO()
    with redirect_stdout(f):
        # exec(request.json['prop']['code'])
        exec(
            request.json["prop"]["code"],
            seesion_mgr.get_session(request.json["session_id"]).my_module.__dict__,
        )
    s = f.getvalue()

    import ast, pandas

    tree = ast.parse(request.json["prop"]["code"], "script_path", "exec")
    body = getattr(tree, "body")
    last_node = body[-1]
    if type(last_node) is ast.Expr:
        if "id" in last_node.__dict__["value"].__dict__:
            id = last_node.__dict__["value"].__dict__["id"]
            last_node_value = getattr(my_module, id)
            print(type(last_node_value))
            if isinstance(last_node_value, pandas.DataFrame):
                s = last_node_value.head(20).to_html()
                return {"res": s, "type": "table"}
    # with open('app.json', 'r') as f:
    #     try:
    #         app_json = json.loads(f.read())
    #     except:
    #         app_json = {}
    #     app_json[request.json['wid']]['block']['prop']['last_run_result'] = s
    # with open('app.json', 'w') as f:
    #     f.write(json.dumps(app_json))
    return {"res": s}


def get_df_column():
    code = request.args.to_dict()
    print(code)
    return {"res": exec("df.col1", runtime.get_module().__dict__)}


def run_query_block():
    query = request.json["prop"]["query"]
    import sqlite3
    import pandas as pd

    cnx = sqlite3.connect("file.db")
    print(runtime.get_main_class().__dict__)
    return {"res": pd.read_sql(query, cnx).to_html()}


@overload
def update_var(event):
    setattr(my_module, event["prop"]["value_var"], event["payload"])


def update_var(var, value, cls, my_module):
    setattr(my_module, var, value)
    cls.update_app_state(var, value)


def update_var_select(event):
    setattr(my_module, event["prop"]["value_var"], event["payload"])
    getattr(my_module, event["prop"]["on_change"])()


def run_fn():
    session = seesion_mgr.get_session(request.json["session_id"])
    session.main_class.get_app_block_by_id(request.json["id"])
    my_module = session.my_module
    print("name space", dir(my_module))
    main_class = getattr(my_module, session.class_object_name)
    print(session, main_class, my_module)

    """
    clear notification functionality to be redeveloped with context of app session
    """
    # runtime.get_main_class().clear_notifications()

    on_change_type = ["input", "select", "date_input", "slider", "radio_button", "menu"]
    if request.json["type"] == "list" and request.json["payload"]["action"] == "click":
        update_var(
            request.json["prop"]["value_var"],
            request.json["payload"]["value"],
            main_class,
            my_module,
        )
    elif (
        request.json["type"] in on_change_type
        and request.json["payload"]["action"] == "change"
        and request.json["payload"]["value"] is not None
        and request.json["prop"]["value_var"] is not None
    ):
        update_var(
            request.json["prop"]["value_var"],
            request.json["payload"]["value"],
            main_class,
            my_module,
        )
    elif request.json["type"] == "page_link":
        main_class.set_page(request.json["prop"]["data"])

    if "on_change" in request.json["prop"] and request.json["prop"]["on_change"]:
        try:
            fn = getattr(my_module, request.json["prop"]["on_change"])
            print(fn)
            try:
                block = session.main_class.get_app_block_by_id(request.json["id"])
                print("block", block)
                if block["type"] == "chart":
                    fn(request.json["payload"]["value"])
                elif "args" in block["prop"] and block["prop"]["args"] is not None:
                    fn(*tuple(block["prop"]["args"]))
                else:
                    fn()
            except Exception as e:
                print("error", type(e), e)
                # runtime.get_main_class().notification({'type':'error', 'data':str(e), 'status':'active'})
                # fn(request.json)
                # runtime.initialized.send('signal from server')
        except Exception as e:
            logger.debug(
                "function {} not in module".format(request.json["prop"]["on_change"])
            )
            logger.error(e)
    return rerun(main_class, my_module, session)


def fn(method_name):
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    return method


for route in routes:
    app.add_url_rule(route["path"], view_func=fn(route["fn"]), methods=["get", "post"])


def start_server(file_path, host="localhost", port=5000):
    global my_module
    runtime.set_file_path(file_path)
    # runtime.run_script(file_path)
    # my_module = runtime.get_module()

    logger.debug("Starting server...")
    # import webbrowser
    # webbrowser.open('http://127.0.0.1:4200/')
    # app.run(host = host, port = port, debug=False, threaded= True)
    host = "localhost" if host == None else host
    port = 5000 if port == None else port

    serve(app, host=host, port=port)
    logger.debug("Server started on port 5000")


if __name__ == "__main__":
    start_server()
