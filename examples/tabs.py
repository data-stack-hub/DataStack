from datastack import datastack

ds = datastack(main=True)

tab1, tab2 = ds.tabs(["tab1", "tab2"])
# col1, col2 = tab1.columns(2)


# def dummy():
#     col1.write("Button clicked")


# col1.button("click", on_click=dummy)

tab1.subheader("Input value")
count = tab1.input(value=0)
tab1.write("count:" + str(count))
