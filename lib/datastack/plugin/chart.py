import datastack as ds
import plotly.express as px
import pandas as pd


ds.write('Chart builder')
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
df1 = pd.DataFrame(data=d)
df3 = pd.read_csv(r"\\fs02\Engineering\IndiaTeam\Projects\2023Q1_SpeedupLearningCycle\MemoModels\dfcomp_ModelTrainData_1496cells.csv")
# print(df.col1)

# ds.code('','12')
ds.chart_builder()
# ds.chart(px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16]))
