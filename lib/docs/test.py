from datastack import stacker as ds


print("calss id", id(ds))
ds.button("test")

val = ds.select(options=["a", "b", "c"])
ds.write(val)
