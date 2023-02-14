ctx = {}

def set_main_class(cls):
    ctx['main_class'] = cls
    print('ctx',ctx)

def get_main_class():
    return ctx['main_class']