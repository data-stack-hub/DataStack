from flask import jsonify
import datastack as ds
import pandas as pd

# -------------------------------- user py file ------------------------------
def dummy_fn():
    pass
ds.write('wriet')
ds.sidebar().write('in sidebar')
# ds = datastack()

def load_page1(a):
    ds.set_page('/page1')

def load_main_page(a):
    ds.set_page('main_page')
#  user defined functions and script

# pages
ds.sidebar().button('Page1', on_click=load_page1)
page1 = ds.page('/page1')
page1.write('This is new page')
page1.button('go to main page', on_click=load_main_page)

# sildebar
ds.write('Inside sidebar', location='sidebar')
ds.write('pages', location='sidebar')
ds.write('-------------------------------------', location='sidebar')

# sidebar class
ds.write("sidebar as class method")
ds.sidebar().write('inside sidebar class')
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
# selected_value = 'b'
selected_value = ds.select(['a','b','c'], on_change=dummy_fn )
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

# outOfOrder Container
ds.write('Out of order container')
container = ds.container()
container.write('inside the container')
ds.write('out side the container')
container.write('inside the container again ')
ds.write('-------------------------------------')

# Expander
expander = ds.sidebar().expander('expander')
expander.write('this is inside the expander from py')
ds.sidebar().write('-------------------------------------')
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







