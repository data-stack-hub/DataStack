import inspect
class datastack():
    def __init__(self):
        self.app=[]
        self.blocks = []
        self.count = 0


#  change to on_click = function name and on_click_source = function code
#  move frame logic to somewhere else
    def button(self, name, on_click=''):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        # print('button_args', args)
        if on_click :
            click_fn = inspect.getsource(on_click)
            click_fn_name = args[1].split("=")[1]
        else:
            click_fn =''
            click_fn_name =''

        component = {
            "id":1,
            "type":'button',
            "prop":{
                "title":name,
                "on_click":click_fn,
                "on_click_name":click_fn_name,
                "title_args":args[0]
            }
        }
        self.blocks.append(component)

    def input(self,value):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        component = {
            "id":50,
            "type":"input",
            'prop':{
                "value":value,
                "input_var":args[0],
                "on_click":"update_var",
                "on_click_name":"update_var",

            }
        }
        self.blocks.append(component)

    def select(self, options, value):
        # list options args to be corrected
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('value=') + 6:-1].split(',')
        # print('selected arge',type(args), args)
        component = {
            "id":60,
            "type":"select",
            "prop":{
                "options":options,
                # "options_frm":args[0],
                "value":value,
                "value_frm":args[0].replace(' ',''),
                "on_click":"update_var_select",
                "on_click_name":"update_var_select"
            }
        }
        # print('selec comp', component)
        self.blocks.append(component)

    # test
    def select_t(self, options):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('value=') + 6:-1].split(',')
        component = {
            "id":60,
            "type":"select_t",
            "prop":{
                "options":options,
                # "options_frm":args[0],
                "value":'',
                "value_frm":'',
                "on_click":"update_var_select",
                "on_click_name":"update_var_select"
            }
        }
        # print('selec comp', component)
        self.blocks.append(component)
        def r_fn(a):
            return a
        return r_fn

    def list(self, data, on_click='', location=''):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('on_click=') + 9:-1].split(',')
        args_options = string[string.find('(')+1:string.find(', on_click=')]
        # .replace(',','').replace(' ','')
        if on_click :
            click_fn = inspect.getsource(on_click)
            click_fn_name = args[0]
        else:
            click_fn =''
            click_fn_name =''
        component = {
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

        self.blocks.append(component)


    def write(self, data,  location=''):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        component = {
            "id":100,
            "type":'text',
            "location":location,
            "prop":{
                "data":data,
                "args":args[0]
            }
        }
        self.blocks.append(component)

    def html(self, html):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')

        component = {
            "id":200,
            "type":'html',
            "prop":{
                "data":html,
                'args':args[0]
            }
        }
        self.blocks.append(component)

    def container(self):
        # prevent nesting insider the layout element
        cls = datastack()
        self.blocks.append(cls)
        return cls

    def iframe(self, url):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')

        component = {
            "id":600,
            "type":"iframe",
            "prop":{
                "url":url,
                "url_var":args[0]
            }
        }
        self.blocks.append(component)

    def build_app(self):
        _app =  [ x.blocks if isinstance(x, object) and x.__class__.__name__ =='datastack' else [x] for x in self.blocks]
        self.app = [item for sublist in _app for item in sublist]
        return self.app

    def rerun(self, my_vars, old_app):

        # print('my_vasrs',{k: v for k, v in my_vars.items() if not k.startswith("__")})
        # old_app = self.app.copy()
        # print('old app',old_app)

        for k,v in my_vars.items():
            globals()[k] = v
        self.build_app()
        for c in self.app:
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
        # print(self.app)
        # print('old app',old_app)
        # print('new app',self.app)
        # diff = [x for x in self.app if x not in old_app else x]
        # diff = [x.update(is_change=True) if x not in old_app else x for x in self.app]
        # diff = [{**x, 'is_change':True} if x  not in old_app else {**x, 'is_change':False}  for x in self.app ]

        # print('diff',diff)
        return self.app
    def inc(self):
        self.count = self.count + 1
        return self.count