"""
use any element with or without context manager
for example:
    col1, col2 = ds.columns(2)

    without context manager
    col1.write('col1')
    col2.write('col2')

    or with context manager 
    with col1:
        ds.write('col1')
    with col2:
        ds.write('col2')
"""

class column:
    def __init__(self):
        self.app = []

    def write(self, data):
        self.app.append(data)
        print(self.app)

    def __enter__(self):
        pass

    def __exit__(self,*_):
        pass

class test_ds:
    def __init__(self):
        self.app = []

    def write(self, data):
        self.app.append(data)
        print(self.app)

    def columns(self):
        return column(), column()

ds = test_ds()
col1, col2 = ds.columns()

col1.write('col1')
col2.write('col2')

with col1:
    print('col1')

    
