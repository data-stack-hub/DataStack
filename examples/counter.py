from datastack import datastack
ds = datastack(main=True)

ds.subheader('DataStack click counter app')

count = 0 

def inc_count():
    global count
    count += 1

ds.button('Click', on_click=inc_count)
ds.write('counts: ' + str(count))