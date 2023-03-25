import importlib, os
from datastack.server import utils
from datastack.logger import logger
ctx = {}

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

def run_script(path):
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
    from io import StringIO
    from contextlib import redirect_stdout
    f = StringIO()
    # with redirect_stdout(f):
    # exec(code, my_module.__dict__)
    # get_main_class().write(f.getvalue())

    """
        execute script with ast node
    """
    import ast
    tree = ast.parse(filebody, path, "exec")
    body = getattr(tree, "body")
    for i, node in enumerate(body):
        if (type(node) is ast.With):
            if node.items[0].context_expr.func.attr == 'code_block':
                import astunparse
                code_body = astunparse.unparse(node.body)
                
                new_node = ast.Expr(
                    value =ast.Call(
                    func = ast.Attribute(
                    attr="callback",
                    value=ast.Name(id='ds',ctx=ast.Load()),
                    ctx=ast.Load()
                    ),
                args=[node.items[0].context_expr.args[0], ast.Str(s=code_body)],
                keywords=[]
                )
                )
                print(node.items[0].context_expr.args)
                print(ast.dump(node))
                del body[i]
                body.insert(i,new_node)
                # print(ast.dump(node))
                # print(code_body)
                # exec(code_body, {})
        if (type(node) is ast.Expr):
            if (type(node.value) == ast.Call and 'attr' in node.value.func.__dict__ and node.value.func.attr=='callback'):
                # if node.value.func.attr == 'callback':
                    print(ast.dump(node))
                    pass
    # print(len(getattr(tree, "body")), body)
    tree = ast.fix_missing_locations(tree)
    code = compile(tree, path, "exec")
    with redirect_stdout(f):
        exec(code, my_module.__dict__)

    update_module(my_module)
    print(f.getvalue())
def create_session():
    """
    check if session is available with session id
    create session if not available - class
    id,script data, state, script runner, user info, session state
    """
    reset_main_class()
    run_script(get_file_path())
    return 'session_id'