from flask import jsonify
import datastack as ds
import pandas as pd

# -------------------------------- user py file ------------------------------
def dummy_fn():
    pass

ds.header('DataStack Components')


def load_page1(a):
    ds.set_page('/page1')

def load_main_page(a):
    ds.set_page('main_page')
#  user defined functions and script


# sildebar
ds.sidebar().subheader('Pages')

# pages
# ds.sidebar().button('Page1', on_click=load_page1)
some_var = ds.sidebar().list(['page1', 'page2'], on_click=load_page1)
page1 = ds.page('/page1')
page1.write('This is new page')
page1.button('go to main page', on_click=load_main_page)
ds.sidebar().divider()

# columns
ds.subheader('Columns')
col1, col2, col3  = ds.columns(3)
col1.write('col1')
col2.write('col2')

col1.write('col1 text')
col2.write('col2 text')

col3.write('col3')
col1.button('click')

# dataframe
ds.subheader('dataframe')
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])
ds.dataframe(df)
col3.html(df.to_html())

# list
ds.subheader('List')
def list_click(a):
    global selection_from_list
    selection_from_list = a['payload']
    print(a)

selection_from_list = ''
ds.list(['a','b','c'], on_click=list_click)
ds.write('Selected Option: ' + selection_from_list)
ds.divider()

#  dropdown
ds.subheader('Dropdown Selection')
selected_value = ds.select(['a','b','c'], on_change=dummy_fn )
ds.write('selected value: ' + selected_value)
ds.divider()



#  dropdown in sidebar
ds.divider()
ds.sidebar().subheader('Dropdown Selection')
selected_value_sidebar = ds.sidebar().select(['a','b','c'], on_change=dummy_fn )
ds.sidebar().write('selected value: ' + selected_value_sidebar)
ds.sidebar().divider()

#  dropdown in container
container = ds.container()
container.subheader('Dropdown Selection - container')
selected_value_container = container.select(['a','b','c'], on_change=dummy_fn )
container.write('selected value: ' + selected_value_container)
ds.divider()

# Button
def inc_count(a):
    global count
    count +=1
ds.subheader('Button click')
count = 0
ds.button('Click', on_click=inc_count)
ds.write('Count value: '+ str(count))
ds.divider()

# input
ds.subheader('Input value')
input_value = 'default value'
ds.input(input_value)
ds.write('Input: '+ input_value)
ds.divider()

# code
ds.subheader('code')
ds.code("print(count)", key = 'mycode')
ds.divider()

# query
ds.subheader('SQL Query')
ds.query("""select 1 as a, 2 as b, 3 as c
union all
select 4 as a, 5 as b, 6 as c""")
ds.divider()


#  HTML
ds.subheader("HTML")
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])

ds.html(df.to_html())
ds.html("<div style='color:green'>HTML Text</div>")
ds.divider()

# outOfOrder Container
ds.subheader('Out of order container')
container = ds.container()
container.write('inside the container')
ds.write('out side the container')
container.write('inside the container again ')
ds.divider()

# Expander
ds.sidebar().subheader('Expander')
expander = ds.sidebar().expander('expander')
expander.write('this is inside the expander from py')
ds.sidebar().divider()

# Iframe
ds.subheader('Iframe')
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
ds.divider()







