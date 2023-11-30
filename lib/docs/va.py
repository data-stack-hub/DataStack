from varname import argname


class elements:
    def __init__(self):
        self.app = []

    def sidebar(self):
        c = elements()
        self.app.append(c)
        return c

    def button(self, name):
        # print("Button name:", argname("name"))
        self.app.append({"type": "button", "name": argname("name")})


ds = elements()
ds.sidebar().button("test button")
for b in ds.app:
    print(b, b.__dict__)


from pathlib import Path

code = "ds.button('test button')"
sourcefile = "v1.py"
Path(sourcefile).write_text(code)
compiled = compile(code, sourcefile, mode="exec")
exec(compiled)
# exec("ds.button('test')")
