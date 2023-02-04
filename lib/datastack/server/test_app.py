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
    return jsonify(ds.build_app())

def rerun():
    global a1
    a1 = {k: v for k, v in globals().items() if not k.startswith("__")}
    return jsonify(ds.rerun(a1, {}))


def update_var_select(aaa):
    globals()[aaa['prop']['value_frm']]=aaa['payload']

def update_var(aaa):
    globals()[f"input_value"]=aaa['payload']


#  user defined functions and script

# sildebar
ds.write('Inside sidebar', location='sidebar')
ds.write('-------------------------------------', location='sidebar')

# list
ds.write('List')
def list_click(a):
    global selection_from_list
    selection_from_list = a['payload']
    print(a)

selection_from_list = ''
ds.list(['a','b','c'], on_click=list_click)
ds.write('Selected Option: ' + selection_from_list)
ds.write('-------------------------------------')

#  dropdown
ds.write('Dropdown Selection')
selected_value = 'b'
ds.select(['a','b','c'], value=selected_value )
ds.write('selected value: ' + selected_value)
ds.write('-------------------------------------')

# Button
def inc_count(a):
    global count
    count +=1
ds.write('Button click')
count = 0
ds.button('Click', on_click=inc_count)
ds.write('Count value: '+ str(count))
ds.write('-------------------------------------')

# input
ds.write('Input value')
input_value = 'default value'
ds.input(input_value)
ds.write('Input: '+ input_value)
ds.write('-------------------------------------')

#  HTML
ds.write("HTML")
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])

ds.html(df.to_html())
ds.html("<div style='color:green'>HTML Text</div>")
ds.write('-------------------------------------')

# outoforder
ds.write('Out of order')
container = ds.container()
container.write('inside the container')
ds.write('out side the container')
container.write('inside the container again ')
ds.write('-------------------------------------')

# Iframe
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
ds.write('-------------------------------------')







