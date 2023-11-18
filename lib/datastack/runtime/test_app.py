from datastack import datastack
ds2 = datastack(main=True)


def dummy():
    pass
ds2.header('App')
test_var = ds2.input('test', on_change=dummy)
ds2.header(test_var)
ds2.button('test', on_click=dummy)