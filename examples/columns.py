from datastack import datastack

ds = datastack(main=True)

col1, col2 = ds.columns(2)

col1.write("col1")
col2.write("col2")
