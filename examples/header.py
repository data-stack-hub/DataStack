from datastack import datastack

ds = datastack(main=True)

tab1, tab2 = ds.tabs(["tab1", "tab2"])
tab1.subheader("this is subheader", id="id")


def update_header():
    tab1.subheader("this is new subheader", id="id")


# ds.button('update header', on_click=update_header)
update_header()
