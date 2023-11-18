from datastack import datastack
import pandas as pd
from cachetools import TTLCache
import pyodbc

ds= datastack(main=True)
ds.header('This is Test app')

cnxn = pyodbc.connect(driver='{SQL Server}', server='DBCLUSTER02', database='ETestData',               
               trusted_connection='yes')

@ds.cache_data
def get_data(a):
    df = pd.read_sql("select top 10000 * from testraw", cnxn)
    return df

ds.table(get_data('test1'))