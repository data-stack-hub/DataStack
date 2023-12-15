from datastack import datastack
import pandas as pd
import numpy as np

ds = datastack(main=True)

nrows = 7 * 24
df = pd.util.testing.makeTimeDataFrame(nrows, freq="H")
df["id"] = np.arange(df.shape[0])
ds.table(df)
