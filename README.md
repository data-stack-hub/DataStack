
<img src="lib/docs/images/image-3.png" width="100">

# Welcom to DataStack

**The Fastes way to build apps in python**

Datastack is an open-source framework that enables you to easily build real-time web apps, internal tools, dashboards, weekend projects, data entry forms, or prototypes using just Python—no frontend experience required.

## Installation

```
pip install git+https://github.com/data-stack-hub/DataStack.git#subdirectory=lib
```
or 

```bash
git clone https://github.com/data-stack-hub/DataStack.git
cd DataStack\lib
pip install .
```
## Quickstart

Create new file `counter.py` with following code:

```python
from datastack import datastack
ds = datastack(main=True)

ds.subheader('DataStack click counter app')

count = 0 

def inc_count():
    global count
    count += 1

ds.button('Click', on_click=inc_count)
ds.write('counts: ' + str(count))
```

Now run it to open the app!
```
$ datastack run counter.py
```

Open app in browser `localhost:5000`

![Alt text](<lib/docs/images/counter.gif>)



# DataStack Widgets


```python
# write text
ds.write('some text')
```

```python
#  dropdown selection
ds.subheader('Dropdown Selection')
selected_value = ds.select(['a','b','c'])
ds.write('selected value: ' + selected_value)

```

```python
# list
ds.subheader('List')
selection_from_list = ds.list(['a','b','c'])
ds.write('Selected Option: ' + selection_from_list)
```

```python
# Button
def inc_count(a):
    global count
    count +=1
ds.subheader('Button click')
count = 0
ds.button('Click', on_click=inc_count)
ds.write('Count value: '+ str(count))

```

```python
# input
ds.subheader('Input value')
input_value = ds.input(input_value)
ds.write('Input: '+ input_value)

```

```python
#  HTML
ds.subheader("HTML")
ds.html("<div style='color:green'>HTML Text</div>")

```

```python
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


```python
# page divider
ds.divider()
```

```python
# dataframe
df = pd.DataFrame(
    [["a", "b"], ["c", "d"]],
    index=["row 1", "row 2"],
    columns=["col 1", "col 2"])
ds.write('dataframe')
ds.dataframe(df)
```

```python
# table
ds.write('table')
ds.table(df)
```

```python
# data input
date = ds.date_input()
```