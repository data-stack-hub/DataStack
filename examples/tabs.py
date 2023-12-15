from datastack import datastack

ds = datastack(main=True)

tab1, tab2 = ds.tabs(["tab1", "tab2"])
col1, col2 = tab1.columns(2)


def dummy():
    col1.write("Button clicked")


col1.button("click", on_click=dummy)

# col2.write('col2')
