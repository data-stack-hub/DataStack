from flask import jsonify
from ds_class import datastack
import pandas as pd

# -------------------------------- user py file ------------------------------
def dummy_fn(a):
    pass

ds = datastack()

#  this should be moved to ds class
def test():
    print(ds.app)
    return jsonify(ds.app)

def rerun():
    global a1
    a1 = {k: v for k, v in globals().items() if not k.startswith("__")}
    return jsonify(ds.rerun(a1, {}))


def update_var_select(aaa):
    globals()[aaa['prop']['value_frm']]=aaa['payload']

def update_var(aaa):
    globals()[f"input_value"]=aaa['payload']


#  user defined functions and script

ds.write('List')
def list_click(a):
    global selection_from_list
    selection_from_list = a['payload']
    print(a)

selection_from_list = ''
ds.list(['a','b','c'], on_click=list_click)
ds.write('Selected Option: ' + selection_from_list)
ds.write('-------------------------------------')

ds.write('Dropdown Selection')
selected_value = 'b'
ds.select(['a','b','c'], value=selected_value )
ds.write('selected value: ' + selected_value)
ds.write('-------------------------------------')


def inc_count(a):
    global count
    count +=1
ds.write('Button click')
count = 0
ds.button('Click', on_click=inc_count)
ds.write('Count value: '+ str(count))
ds.write('-------------------------------------')

ds.write('Input value')
input_value = 'default value'
ds.input(input_value)
ds.write('Input: '+ input_value)
ds.write('-------------------------------------')

ds.write("HTML")
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])

ds.html(df.to_html())
ds.html("<div style='color:green'>HTML Text</div>")
ds.write('-------------------------------------')

ds.write('Iframe')
def change_iframe(a):
    global url
    if a['payload'] == 'Wikipedia':
        url = 'https://www.wikipedia.org/'
    elif a['payload'] == 'ML':
        url = 'https://en.wikipedia.org/wiki/ML'
    else:
        url = 'https://www.wikipedia.org/'
        
ds.list(['Wikipedia','ML'], on_click=change_iframe)
url = 'https://www.wikipedia.org/'
ds.iframe(url)


# global inc
# def inc():
#     global count,z
#     count = count + 1
#     z= 'test1'
#     return count + 1

# def add_button():
#     ds.button('dynamic button')
#     print('buttoneede')
# def d_fn(val):
#     return val + '_d_fn'

# ds.write('List')
# ds.list(['a','b','c'], on_click=dummy_fn)
# # ds.write()

# ds.write('Iframe')
# ds.iframe('https://www.wikipedia.org/')

# count = 0
# button_text = 'click'
# ds.button(button_text, on_click=inc)
# ds.button('add button', on_click=add_button)
# ds.write('this is count'+str(count))
# input_value = 'abcd'
# ds.input(input_value)
# ds.write('dynamic input value: '+ input_value)

# selected_value = 'b'
# ds.select(['a','b','c'], value=selected_value )
# ds.write('selected value: ' + selected_value)



# # test: a = ds.select_t([a,b,c]) ; print(a)
# # selected_option_t = ds.select_t(['x','y','z'])
# # ds.write(selected_option_t)
# z= 'test'
# ds.write(d_fn(z))

# df = pd.DataFrame(
#     [["a", "b"], ["c", "d"]],
#     index=["row 1", "row 2"],
#     columns=["col 1", "col 2"],
# )
# df1 = pd.DataFrame(
#     [["a", "b"], ["c", "d"]],
#     index=["row 1", "row 2"],
#     columns=["df1_col 1", "df1_col 2"],
# )
# print(df)
# ds.html(df.to_html())

# # r_df = fn.pilot_yield_data(fn.pilot_yield_query('2023-01-21', '2023-01-28'))
# # ds.html(r_df.to_html())
# # def test1(click=False):
# #     global my_vars

# #     global count

# #     def inc(count):
# #         ds.write('dynamic write in function')
# #         return count + 1
# #     global  d_fn
# #     def d_fn(val):
# #         return val + '_d_fn'
# #     if not click:
# #         count = 0
# #         def inc():pass
# #         a = ds.button('click', on_click=inc)
# #         ds.button('click', on_click=inc)
# #         ds.button('click', on_click=inc)
# #         ds.write('this is count'+str(count))
# #         global z
# #         z = 'test'
# #         ds.write(d_fn(z))
# #         if False:
# #             ds.write('True statement')
# #         print(dir())
# #         # if a:
# #         #     ds.write('clicked')
# #         my_vars = dir()
# #         print('vars', my_vars)
# #     if click:
# #         count = inc(count)
# #         z= 'test1'
# #         global a1 
# #         # a1 = {}
# #         # for k,v in globals().items():
# #         #     a1[k] = v
# #         a1 = {k: v for k, v in globals().items() if not k.startswith("__")}
# #         return jsonify(ds.rerun(a1))
# #     return jsonify(ds.app)





