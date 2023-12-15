from datastack import datastack
import plotly.express as px

ds = datastack(main=True)
fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])


tab1, tab2 = ds.tabs(["tab1", "tab2"])
tab1.chart(fig)
