from varname import argname


class elements:
    def sidebar(self):
        return elements()

    def button(self, name):
        print("Button name:", argname("name"))


ds = elements()
ds.sidebar().button("test button")
