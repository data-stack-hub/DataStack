from datastack import datastack

ds = datastack(main=True)


col3, col4 = ds.columns(2)
col3.write("col1")
col4.write("col2")

# container = ds.container()
# container.write('test container')
# col1, col2 = container.columns(2)

# col1.write('col1')
# col2.write('col2')


# ds.write('test')
