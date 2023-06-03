from flask import jsonify
import datastack as ds
import pandas as pd
import datetime
from PIL import Image
import numpy as np
# -------------------------------- user py file ------------------------------
def dummy_fn():
    pass

import threading
print(threading.current_thread())
ds.header('DataStack Components')


ds.subheader('State')
import json
ds.write(json.dumps(ds.state))

def load_main_page():
    ds.set_page('main_page')
#  user defined functions and script


# sildebar
ds.sidebar().subheader('Pages')

# # run code inside the module
# def fn_test(a):
#     print('function test')
# ds.button('test module', on_click=fn_test)


# update widget
ds.write('this is text', id = 'x') 
ds.write('this is updated text', id = 'x')

# pyplot
ds.subheader('PyPlot')
arr = np.random.normal(1, 1, size=100)
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
ds.pyplot(fig)

# image
ds.subheader('Image')
image = Image.open('test_image.jpg')
ds.image(image)
# Date picker
dd_date = ds.date_input(value=datetime.date(2019, 7, 6))
ds.write('Selected_Date '  + str(dd_date))
# slider
values1 = ds.slider(0,150,20)
ds.write('slider value is '  + str(values1))

values2 = ds.slider(0,150,20)
ds.write('slider value is '  + str(values2))

ds.success("Success message")
ds.info("Info message")
ds.warning("Warning message")
ds.error("Error message")

# charts
ds.subheader('Charts')
import plotly.express as px
data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, x='year', y='pop')
ds.chart(fig)
ds.write('supports plotly charts only- for now')
import plotly.express as px

df = px.data.tips()

fig = px.box(df, x="day", y="total_bill", facet_row="smoker")
fig.update_traces(quartilemethod="exclusive", alignmentgroup='df', offsetgroup='fgf') # or "inclusive", or "linear" by default
fig.update_layout(
    boxmode='group'
)
ds.chart(fig)

# pages
ds.sidebar().page_link('main_page')
ds.sidebar().page_link('page1')
ds.sidebar().page_link('page2')
ds.sidebar().page_link('pycaret')

page1 = ds.page('page1')
page1.write('This is new page')
page1.button('go to main page', on_click=load_main_page)

page2 = ds.page('page2')
page2.write('This is new page')
page2.button('go to main page', on_click=load_main_page)
ds.sidebar().divider()

pc = ds.page('pycaret')
pc.header('PyCaret')
page2.button('go to main page', on_click=load_main_page)
# columns
ds.subheader('Columns')
col1, col2, col3  = ds.columns(3)
col1.write('col1')
col2.write('col2')

col1.write('col1 text')
col2.write('col2 text')

col3.write('col3')
col1.button('click')


# tabs
ds.subheader('Tabs')
tab1, tab2, tab3 = ds.tabs(["tab1", "tab2", "tab3"])
tab1.write('tab1 text')
tab2.write('tab2 text')
tab3.write('tab3 text')
tab1.button('click')

# dataframe
ds.subheader('dataframe')
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])
ds.dataframe(df)
col3.html(df.to_html())
tab3.html(df.to_html())

# list
ds.subheader('List')
def list_click(a):
    global selection_from_list
    selection_from_list = a['payload']
    print(a)

selection_from_list = ''
selection_from_list = ds.list(['a','b','c', 'd'], on_click=list_click)
ds.write('Selected Option: ' + str(selection_from_list))
ds.divider()

#  dropdown
ds.subheader('Dropdown Selection')
selected_value = ds.select(['a','b','c'], on_change=dummy_fn )
ds.write('selected value: ' + selected_value)
ds.divider()



#  dropdown in sidebar
# ds.divider()
# ds.sidebar().subheader('Dropdown Selection')
# selected_value_sidebar = ds.sidebar().select(['a','b','c'], on_change=dummy_fn )
# ds.sidebar().write('selected value: ' + selected_value_sidebar)
# ds.sidebar().divider()

#  dropdown in container
container = ds.container()
container.subheader('Dropdown Selection - container')
selected_value_container = container.select(['a','b','c'], on_change=dummy_fn )
container.write('selected value: ' + selected_value_container)
ds.divider()

# Button
def inc_count(args_var,args_var1):
    global count
    count +=1
    print(args_var, args_var1)
ds.subheader('Button click')
count = 0
args_var = 't'
args_var1 = 't1'
ds.button('Click', on_click=inc_count, args=(args_var,args_var1,))
ds.write('Count value: '+ str(count))
ds.divider()

# input
ds.subheader('Input value')
input_value = 'default value'
input_value = ds.input(input_value)
ds.write('Input: '+ str(input_value))
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


# HTML
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

site = ds.list(['Wikipedia','ML'], on_click=change_iframe)
url = 'https://www.wikipedia.org/'
ds.iframe(url)
ds.divider()

# pycaret
from pycaret.datasets import get_data
from pycaret.classification import ClassificationExperiment


import matplotlib
matplotlib.use('Agg')


def plot(model, plot_type):
    pc.write('selected plot: ' + ds.state['selected_plot'], id='qwe')
    pc.image(Image.open(s.plot_model(best, plot=ds.state['selected_plot'], save=True)), id=12)
    print('---->',model, plot_type)

def setup(a):
    global  best
    s.setup(data, target = target, session_id = 123)
    best = s.compare_models(include = ['lr'])
    result = s.pull()
    print('result', result)
    pc.dataframe(result)
    # pc.image(Image.open(s.plot_model(best, plot='auc', save=True)))
    available_plots = list(s._available_plots.keys())
    selected_plot = pc.select(list(s._available_plots.keys()), on_change=plot, id='x1', args=('q',az))

def get_data_py(a):
    print('getting data')
    global data, target
    data =  get_data(selected_dataset)
    target = pc.select(data.columns.to_list(), on_change=setup)



# def dum(a):
#     pc.image(Image.open(s.plot_model(best, plot='auc', save=True)))
s = ClassificationExperiment()

datasets = get_data()#['Dataset'].to_list()
az = 'asd1'
# selected_plot = pc.select(list(s._available_plots.keys()), on_change=plot, id='x1', args=('q',az))
selected_exp_type = pc.select(datasets['Default Task'].unique())
selected_dataset = pc.select( datasets[datasets['Default Task'] == selected_exp_type]['Dataset'], on_change=get_data_py)
pc.write('selected dataset is: ' + selected_dataset)




# data =  get_data('diabetes')
# s.setup(data, target = 'Class variable', session_id = 123)
# best = s.compare_models(include = ['lr'])
# pc.button('show chart', on_click=dum)

# pc.image(Image.open(s.plot_model(best, plot='auc', save=True)))


