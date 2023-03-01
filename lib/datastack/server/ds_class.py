import inspect
from contextlib import contextmanager
from datastack.runtime import runtime
from datastack.logger import logger
import uuid
class datastack():
    def __init__(self, type='main_page', path='', title='', main=False):
        self.type = type
        self.path = path
        self.title = title
        self.app={
            'current_page':'main_page',
            'sidebar':[],
            'main_page':[],
            'pages':[],
            'appstate':{"session_id":"default"}
        }
        self.blocks = {
            'sidebar':[],
            'main_page':[],
            'pages':[]
        }
        if main:
            runtime.set_main_class(self)

#  change to on_click = function name and on_click_source = function code
#  move frame logic to somewhere else
    def button(self, name, on_click=''):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        # print(string.replace('.sidebar()',''), string.find('(')+1)
        args = string.replace(".sidebar(",'')[string.find('(')+1 :-1].split(',')
        # print('button_args', args)
        if on_click :
            click_fn = inspect.getsource(on_click)
            click_fn_name = args[1].split("=")[1]
        else:
            click_fn =''
            click_fn_name =''

        block = {
            "id":1,
            "type":'button',
            "prop":{
                "title":name,
                "on_click":click_fn,
                "on_click_name":click_fn_name,
                "title_args":args[0]
            }
        }
        self.append_block(block)

    def input(self,value):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        block = {
            "id":50,
            "type":"input",
            'prop':{
                "value":value,
                "input_var":args[0],
                "on_click":"update_var",
                "on_click_name":"update_var",
            }
        }
        self.append_block(block)

    def divider(self):
        block = {
            "id":0,
            "type":"divider",
            "prop":{}
        }
        self.append_block(block)

    def header(self, data):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        # print(string)
        args = string[string.find('.header(') + 7:-1].split(',')
        block = {
            "id":100,
            "type":'header',
            "prop":{
                "data":data,
                "args":args[0]
            }
        }
        self.append_block(block)

    def subheader(self, data):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        # print(string)
        args = string[string.find('.header(') + 7:-1].split(',')
        block = {
            "id":100,
            "type":'subheader',
            "prop":{
                "data":data,
                "args":args[0]
            }
        }
        self.append_block(block)
    def select(self, options, value='', on_change=''):
        # list options args to be corrected
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('on_change=') + 6:-1].split(',')
        # print('selected arge',type(args), args)
        # print('assigned var', self.get_value_assign_var(inspect.currentframe().f_back))
        if on_change :
            change_fn = inspect.getsource(on_change)
            change_fn_name = string[string.find('on_change=') + 10:-1].split(',')[0].replace("on_change=",'').replace(' ','')
        else:
            change_fn =''
            change_fn_name =''

        block = {
            "id":60,
            "type":"select",
            "prop":{
                "options":options,
                # "options_frm":args[0],
                "value":value,
                # "value_frm":args[0].replace(' ',''),
                'value_frm':self.get_value_assign_var(inspect.currentframe().f_back),
                "on_click":"update_var_select",
                "on_click_name":"update_var_select",
                "on_change_name":change_fn_name
            }
        }
        # print('selec comp', component)
        self.append_block(block)
        return 'default'
    def list(self, data, on_click='', location=''):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('on_click=') + 9:-1].split(',')
        args_options = string[string.find('(')+1:string.find(', on_click=')].replace(').list(','')
        # .replace(',','').replace(' ','')
        if on_click :
            click_fn = inspect.getsource(on_click)
            click_fn_name = args[0]
        else:
            click_fn =''
            click_fn_name =''
        block = {
            "id":500,
            "type":"list",
            "location":location,
            "prop":{
                "list":data,
                "on_click":click_fn,
                "on_click_name":click_fn_name,
                "args_options":args_options
            }
        }

        self.append_block(block)


    def get_value_assign_var(self, f):
        import dis
        """
        # method 1
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        s = inspect.getframeinfo(frame[0])
        code = inspect.currentframe().f_back.f_code
        print('code', dis.code_info(code))

        it = iter(dis.get_instructions(code))
        for instr in it:
            if instr.offset == inspect.currentframe().f_back.f_lasti:
                print('inspect',instr)
                break
        assert instr.opname.startswith('CALL_') 
        print(next(it).argval)       
        """

        # method 2
        import sys
        # f = inspect.currentframe().f_back # get stack frame of caller (depth=1)
        # next op should be STORE_NAME (current op calls the constructor)
        opname = dis.opname[f.f_code.co_code[f.f_lasti+2]]
        # print('opname',opname)
        if opname == 'STORE_NAME' or  opname =='STORE_GLOBAL' : # not all objects will be assigned a name
            # STORE_NAME argument is the name index
            namei = f.f_code.co_code[f.f_lasti+3]
            name = f.f_code.co_names[namei]
            # print('is this?', name)
            return name
        else:
            return None

    def dataframe(self, data):
        block = {
            "id":600,
            "type":"dataframe",
            "prop":{
                "data":data.to_json(orient="records"),
                "columns":list(data.columns)
            }
        }
        self.append_block(block)
        
    def write(self, data,  location=''):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        # print(string)
        args = string[string.find('.write(') + 7:-1].split(',')
        block = {
            "id":100,
            "type":'text',
            "location":location,
            "prop":{
                "data":data,
                "args":args[0]
            }
        }
        self.append_block(block)

    def html(self, html):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')

        block = {
            "id":200,
            "type":'html',
            "prop":{
                "data":html,
                'args':args[0]
            }
        }
        self.append_block(block)

    def editable_html(self, key):
        default_html = [
      {
        "_id": "5f54d75b114c6d176d7e9765",
        "html": "Heading",
        "tag": "h1",
        "imageUrl": "",
      }
    ]
        try:
            import json
            with open('app.json', 'r') as f:
                html = json.loads(f.read())[key]['block']['prop']['html']
        except Exception as e:
            logger.error(e)
            html = default_html
        # if not html:
        #     html = default_html
        logger.info(html)
        block={
            "id":1000,
            'wid':key,
            "type":'editable_html',
            "prop":{
                "html":html
            },
        }
        self.append_block(block)


    def sidebar(self):
        cls = datastack(type='sidebar')
        self.append_block(cls, 'sidebar')
        return cls

    def expander(self, name):
        cls = datastack(type='expander', title=name)
        self.append_block(cls)
        return cls

    # # @classmethod
    # @contextmanager
    def container(self):
        # prevent nesting insider the layout element
        cls = datastack(type ="container")
        self.append_block(cls)
        return cls
    

    def page(self, path):
        cls = datastack(type='page', path=path)
        self.append_block(cls, 'pages')
        return cls

    
    def code(self, data, key):
        block = {
            "id":1200,
            'wid':key,
            "type":"code",
            "prop":{
                "code":data
            }
        }

        with open('app.json', 'r') as f:
            import json
            try:
                b =  json.loads(f.read())
            except:
                b = {}
        if key in b:
            block['prop']['code'] = b[key]['block']['prop']['code']
            block['prop']['last_run_result'] = b[key]['block']['prop']['last_run_result']
        self.append_block(block)
        return ''

    def query(self, data):
        block = {
            "id":1500,
            "type":"query",
            "prop":{
                'query':data
            }
        }
        self.append_block(block)
        return ''
    
    def image(self, data):
        block = {
            "id":1600,
            "type":"image",
            "prop":{
                "data": 'data:image/png;base64, '  + data
            }
        }
        self.append_block(block)

    def iframe(self, url):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')

        block = {
            "id":600,
            "type":"iframe",
            "prop":{
                "url":url,
                "url_var":args[0]
            }
        }
        self.append_block(block)

    def set_page(self, page_name):
        self.app['current_page'] = page_name

    def append_block(self,block, location='main_page'):
        self.blocks[location].append(block)

    def dump_app(self):
        self.app ={
            'current_page':'main_page',
            'sidebar':[],
            'main_page':[],
            'pages':[],
            'appstate':{"session_id":"default"}
        }
        self.blocks = {
            'sidebar':[],
            'main_page':[],
            'pages':[]
        }
    def build_element_from_blocks(self,blocks):
        # with parent
        # return [ dict(each_one, **{'parent':x.type}) for each_one in x.blocks['main_page']] 

        _app =  [ {"id":"", "type":x.type, "title":x.title, "data":x.blocks['main_page']}  if isinstance(x, object) and x.__class__.__name__ =='datastack' and x.type != 'sidebar' else x for x in blocks]
        # return [item for sublist in _app for item in sublist]
        return _app

    def update_state(self):
        def _update_state(location):
          for c in location:
                if c['type'] == 'text' or c['type'] == 'html':
                    c['prop']['data'] = eval(c['prop']['args'])
                if c['type'] == 'button':
                    c['prop']['title'] = eval(c['prop']['title_args'])
                if c['type'] =='select':
                    c['prop']['value'] = eval(c['prop']['value_frm'])
                if c['type'] == 'iframe':
                    c['prop']['url'] = eval(c['prop']['url_var'])
                if c['type'] == 'list':
                    c['prop']['list'] = eval(c['prop']['args_options'])
                if c['type'] == 'expander' or c['type'] == 'container':
                    _update_state(c['data'])
                    pass
                if c['type'] == 'editable_html':
                    default_html = [
      {
        "_id": "5f54d75b114c6d176d7e9765",
        "html": "Heading",
        "tag": "h1",
        "imageUrl": "",
      }
    ]
                    try:
                        import json
                        with open('app.json', 'r') as f:
                            html = json.loads(f.read())[c['wid']]['block']['prop']['html']
                    except Exception as e:
                        logger.error(e)
                        html = default_html
        # if not html:
                    c['prop']['html'] = html
        for location in ['main_page', 'sidebar'] + self.app['pages']:
            _update_state(self.app[location])
    def build_app(self):
        # Transfer blocks to app
        # main page
        # _app =  [ self.build_element_from_cls(x) if isinstance(x, object) and x.__class__.__name__ =='datastack' else [x] for x in self.blocks['main_page']]
        # self.app['main_page'] = [item for sublist in _app for item in sublist]
        self.app['main_page'] = self.build_element_from_blocks(self.blocks['main_page'])

        # all pages
        for page in self.blocks['pages']:
            self.app['pages'].append(page.path)
            # _page = [ x.blocks['main_page'] if isinstance(x, object) and x.__class__.__name__ =='datastack' else [x] for x in page.blocks['main_page']]
            # self.app[page.__dict__['path']] = [item for sublist in _page for item in sublist]
            self.app[page.__dict__['path']] = self.build_element_from_blocks(page.blocks['main_page'])

        #  sidebar
        _app =  [x.blocks['main_page'] if isinstance(x, object) and x.__class__.__name__ =='datastack' else [x] for x in self.blocks['sidebar']]
        # # if any class in sidebar
        # # _app = [a[0] for a in _app]
        # _app =  self.build_element_from_blocks(_app)
        # print(_app)
        # self.app['sidebar'] = [ item for sublist in _app for item in sublist]
        t = self.build_element_from_blocks([a[0] for a in _app])
        self.app['sidebar'] = t

        return self.app

    def rerun(self, my_vars, old_app):

        for k,v in my_vars.items():
            globals()[k] = v

        self.build_app()
        self.update_state()
        # old_app = self.app.copy()

        # diff = [x for x in self.app if x not in old_app else x]
        # diff = [x.update(is_change=True) if x not in old_app else x for x in self.app]
        # diff = [{**x, 'is_change':True} if x  not in old_app else {**x, 'is_change':False}  for x in self.app ]
        # print(self.blocks)
        return self.app
