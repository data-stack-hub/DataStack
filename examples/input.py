from datastack import datastack

ds = datastack(main=True)

ds.subheader("Input value")
count = ds.input(value=0)
ds.write("count:" + str(count))
