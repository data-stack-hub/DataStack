

run python server
```
git clone https://github.com/data-stack-hub/data-stack-rdf.git
cd data-stack-rdf\lib
pip install --editable .
datastack run test_app.py
datastack run test_app.ipynb
```
open http://localhost:5000


examples 
- lib\test_app.py
- lib\test_app.ipynb


```
# write text
import datastack as ds
ds.write('some text')
```

```
#  dropdown selection
ds.subheader('Dropdown Selection')
selected_value = ds.select(['a','b','c'], on_change=dummy_fn )
ds.write('selected value: ' + selected_value)
ds.divider()
```

```
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
```

```
# Button
def inc_count(a):
    global count
    count +=1
ds.subheader('Button click')
count = 0
ds.button('Click', on_click=inc_count)
ds.write('Count value: '+ str(count))
ds.divider()
```

```
# input
ds.subheader('Input value')
input_value = 'default value'
ds.input(input_value)
ds.write('Input: '+ input_value)
ds.divider()
```

```
#  HTML
ds.subheader("HTML")
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])

ds.html(df.to_html())
ds.html("<div style='color:green'>HTML Text</div>")
ds.divider()
```

```
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
```


```
# page divider
ds.divider()
```

```
# dataframe
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])
ds.write('dataframe')
ds.dataframe(df)
```

```
# data input
df = ds.date_input()
```