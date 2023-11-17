import uuid
from datastack.server.ds_class import datastack
import importlib, os, threading
from datastack.server import ds_class
from datastack.runtime import runtime
from datastack.logger import logger
from datastack.server import utils
from pathlib import Path
import sys
from io import StringIO
from contextlib import redirect_stdout


class SessionManager():
    """
    A session manager is used to manage all sessions
    """
    def __init__(self) -> None:
        self.active_sessions = {}

    def connect_session(self):
        #  check if session is exist
        session = AppSession(runtime.get_file_path())
        self.active_sessions[session.id] = {'session':session}
        return session
        
    def get_session(self, id):
        return self.active_sessions[id]['session']

class AppSession():
    """
    contains data for single browser tab
    """
    def __init__(self, file_path) -> None:
        self.id = str(uuid.uuid4())
        self.script_path  = file_path
        self.script_thread = threading.Thread(
            target = self.run_script,
            name='script_thread'
        )
        setattr(self.script_thread, 'session_id', self.id)
        self.script_thread.start()
        self.script_thread.join()
        # for c in runtime.return_collect_cls():
        #     if c.__dict__['session_id'] == self.id:
        #         self.main_class = c
        self.my_module = getattr(self.script_thread, 'my_module')
        # print('my module post ', self.my_module.__dict__)
        # print('post vars',{k: v for k, v in self.my_module.__dict__.items() if not k.startswith("__")})
        for a,b in {k: v for k, v in self.my_module.__dict__.items() if not k.startswith("__")}.items():
            # print(type(b) == datastack , type(b), a,b)
            if type(b) == datastack and b.main:
                self.class_object_name = a
                self.main_class = getattr(self.my_module, self.class_object_name)


        # print('ds from thread', getattr(self.script_thread, 'ds'))
        # cls = getattr(self.script_thread, 'ds')
        # print('type: ', cls.build_app())
        # print('runtime', runtime.return_collect_cls())

        # print(runtime.get_main_class.__dict__)
        # print('thread attrib', getattr(self.script_thread, 'main'))

   
    def trashed_run_script(self):
        print('script_thread: ',threading.current_thread(), )
        print('thread var set', getattr(threading.current_thread(), 'session_id'))
        with open(r'C:\Users\vvora\Desktop\vishal_vora\projects\exp\ds\lib\datastack\runtime\test_app.py') as f:
            filebody = f.read()
        code = compile(filebody,filename=r'C:\Users\vvora\Desktop\vishal_vora\projects\exp\ds\lib\datastack\runtime\test_app.py', mode="exec",flags=0,dont_inherit=1,optimize=-1)
        spec = importlib.util.spec_from_loader('my_module', loader=None)
        my_module = importlib.util.module_from_spec(spec)
        exec(code, my_module.__dict__)
        # setattr(threading.current_thread(), 'ds', getattr(my_module, 'ds'))
        setattr(threading.current_thread(), 'my_module', my_module)

        # print('get attr from module: ', getattr(my_module, 'ds'))
        # print('moduel', my_module.__dict__)
        # print(getattr(getattr(my_module, 'ds'),'ds_class'))
        print(filebody)

    def run_script(self):
        script_path = self.script_path
        logger.info('Script run init')
        if os.path.splitext(script_path)[1] == '.ipynb':
            filebody = utils.read_notebook(script_path)
        else:
            with open(script_path) as f:
                filebody = f.read()

        try:
            code = compile(filebody,filename=script_path, mode="exec",flags=0,dont_inherit=1,optimize=-1)
        except Exception as e:
            logger.error('script failed with error: %s',e)

        spec = importlib.util.spec_from_loader('my_module', loader=None)
        my_module = importlib.util.module_from_spec(spec)

        abs_script_path = os.path.abspath(script_path)
        script_folder = os.path.dirname(abs_script_path)
        sys.path.insert(0,os.path.dirname(abs_script_path))
        try:
            exec(code, my_module.__dict__)
        except Exception as e:
            logger.error('script failed with erroe ',e)
        setattr(threading.current_thread(), 'my_module', my_module)

