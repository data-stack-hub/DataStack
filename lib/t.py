##Python .py code from .jpynb:
# imports
import sys
sys.path.append(r'\\fs02\Engineering\IndiaTeam\Projects\vvora\sm')
from data_stack import sql, datasets, report, email_smtp, chart
from enovix_sm import fn

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

# config
pd.set_option("display.precision", 3)
pd.options.plotting.backend = "plotly"
icells = 'TM24223'
raw_df = sql.run_query("select cellid, cycle, fade from cyclingbycycledata where cellid = 'TM24223' and cycle > 70", 'db03', 'testdata')
# import plotly.graph_objs as go
# # import plotly.plotly as py
# x = raw_df.cycle
# y = raw_df.fade

# z = np.polyfit(x,y,1)
# f = np.poly1d(z)
# print(z)
# other_x = list(range(250,500))
# other_y = f(other_x)

# # calculate new x's and y's
# x_new = np.linspace(0, 10, 50)
# y_new = f(x_new)

# # Creating the dataset, and generating the plot
# trace1 = go.Scatter(
#     x=x,
#     y=y,
#     mode='markers',
#     name='Data',
#     marker=dict(
#         size=3
#     )
# )

# trace2 = go.Scatter(
#     x=other_x,
#     y=other_y,
#     name='Extrapolated Fade',
#     mode='markers',
#     marker=dict(
#         symbol='square-open',
#         size=3
#     )
# )

# layout = go.Layout(
#     title='Fade Extrapolation ',
# )

# data2 = [trace1, trace2]
# fig2 = go.Figure(data=data2, layout=layout)
# fig2
# from sklearn.linear_model import LinearRegression
# X = np.array(df['cycle']).reshape(-1, 1)
# y = np.array(df['fade']).reshape(-1, 1)
# regr = LinearRegression()
# regr.fit(X, y)

# plt.scatter(X, y,  color='black')
# plt.plot(x, regr.predict(X), color='blue', linewidth=3)

# plt.show()
def extrapolate_fade(raw_df, cycle_number, r ='fig'):
#     raw_df = sql.run_query("select cellid, cycle, fade from cyclingbycycledata where cellid = '{}' and cycle > 70".format(cellid), 'db03', 'testdata')
    import plotly.graph_objs as go
    # import plotly.plotly as py
    x = raw_df.cycle
    y = raw_df.fade

    z = np.polyfit(x,y,1)
    f = np.poly1d(z)
    
    other_x = list(range(100,600))
    other_y = f(other_x)
    print('fade at cycle {} - {}'.format(cycle_number, other_y[other_x.index(cycle_number)]))
    
    if r == 'cycle':
        d = pd.DataFrame({"cycle":other_x, "fade":other_y})
        return d[d['fade']>0.2]['cycle'].iloc[0]
    
    else:
        # Creating the dataset, and generating the plot
        trace1 = go.Scatter(
            x=x,
            y=y,
            mode='markers',
            name='Data',
            marker=dict(
                size=3
            )
        )

        trace2 = go.Scatter(
            x=other_x,
            y=other_y,
            name='Extrapolated Fade',
            mode='markers',
            marker=dict(
                symbol='square-open',
                size=3
            )
        )

        layout = go.Layout(
            title='Fade Extrapolation ',
        )

        data2 = [trace1, trace2]
        fig2 = go.Figure(data=data2, layout=layout)
    return fig2
    
def interpolate_fade(df, cycle_number, r='fig'):
    
    
    X = np.array(df['cycle']).reshape(-1, 1)
    y = np.array(df['fade']).reshape(-1, 1)

#     from sklearn.linear_model import LinearRegression
#     regr = LinearRegression()
    
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.datasets import make_regression
    regr = RandomForestRegressor(max_depth=10, random_state=0)
    
    regr.fit(X, y)
    print('fade at cycle {} - {}'.format(cycle_number, regr.predict([[cycle_number]])))
    if r == 'cycle':
#         d= pd.DataFrame({"cycle":X})
        df['fade_pre'] = regr.predict(X)
        print(df)
        return df[df['fade_pre']>0.2]['cycle'].iloc[0]
    else:
        
        import plotly.graph_objs as go
        trace1 =go.Scatter(x=df.cycle,y=df.fade)
        trace2 =go.Scatter(x=df.cycle,y=regr.predict(X))
        trace3 =go.Scatter(x=df.cycle,y=df.fade_)
        data2 = [trace1, trace2, trace3]
        layout = go.Layout(
            title='Fade Interpolation ',
        )
        fig2 = go.Figure(data=data2, layout=layout)
        return fig2
#     return px.scatter(x=df.cycle,y=df.fade)
#     pd.plot.scatter(X, y,  color='black')
#     pd.plot(X, regr.predict(X), color='blue', linewidth=3)

#     plt.show()
    
cellid = 'TM24646'
raw_df = sql.run_query("select cellid, cycle, fade from cyclingbycycledata where cellid = '{}' and cycle > 70".format(cellid), 'db03', 'testdata')
raw_df['fade_']= raw_df['fade']
# raw_df['fade'] =raw_df['fade'].rolling(10).mean()
# raw_df['diff'] = abs(raw_df['fade_'] - raw_df['fade'])
# raw_df.loc[raw_df["diff"] > 0.01, 'fade'] = np.nan

interpolate_fade(raw_df.dropna(),150, r='cycle')
# print(extrapolate_fade(raw_df,500, r='cycle'))
cells =['TM23354','TM23351','TM23348','TM23041','TM23035','TM23034','TM23883','TM23877','TM23428','TM23425','TM23420','TM23416','TM24912','TM24770','TM24765','TM24764','TM24763','TM24185','TM24181','TM24180','TM24178','TM24118','TM24116','TM24106','TM25265','TM25262','TM25261','TM25259','TM25258','TM24654','TM24653','TM24651','TM24650','TM24649','TM24646','TM24645','TM24644','TM24643','TM24639','TM24638','TM24632','TM24627','TM24626','TM24477','TM24465','TM24461','TM24452','TM24447','TM24444','TM24437','TM24223','TM24216','TM24214','TM27328','TM27325','TM27107','TM27105','TM27118','TM26772','TM26784','TM27792','TM27791','TM27788','TM27899','TM27898','TM27894','TM27798','TM27797','TM27796','TM27795','TM27794','TM28195','TM28793','TM28185','TM28178','TM28171','TM28167','TM28166','TM28165','TM28164','TM28161','TM29706','TM29705','TM29704','TM29703','TM29701','TM29420','TM29419','TM29418','TM30169','TM30166','TM28910','TM28907','TM28917','TM28915','TM28913','TM30446','TM31406','TM30035','TM30250','TM30254','TM31405','TM31380','TM29775','TM29774','TM29766','TM29757','TM30150','TM30149','TM30409','TM30408','TM30407','TM30411','TM31135','TM30184','TM30375','TM30374','TM30373','TM30372','TM30369','TM31460','TM31459','TM31458','TM31543','TM31576','TM31592','TM31590','TM31581','TM31580','TM31589','TM31586','TM31609','TM30330','TM31097','TM31095','TM31121','TM31118','TM31110','TM30231','TM30218','TM30205','TM30055','TM30328','TM30326','TM30324','TM33966','TM32644','TM32643','TM32602','TM32660','TM32659','TM32653','TM32622','TM32609','TM32607','TM32510','TM30531','TM30514','TM30500','TM30536','TM30534','TM30511','TM30275','TM30273','TM30263','TM30262','TM30260','TM30259','TM30982','TM30981','TM30977','TM31399','TM31398','TM31298','TM31295','TM31294','TM31292','TM31485','TM31481','TM31688','TM31687','TM31686','TM31685','TM31683','TM32025','TM32024','TM32023','TM31480','TM31479','TM31477','TM31476','TM31469','TM31464','TM36795','TM36793','TM36782','TM32334','TM32367','TM32129','TM32248','TM32247','TM32246','TM32245','TM32243','TM32235','TM32234','TM32233','TM32231','TM32230','TM36892','TM36905','TM36904','TM36912','TM36909','TM36908','TM37335','TM37334','TM37333','TM37331','TM37615','TM37502','TM37501','TM36929','TM36523','TM36520','TM36391','TM34495','TM34476','TM32326','TM32302','TM32366','TM32361','TM32356','TM32349','TM32102','TM32174','TM32143','TM31912','TM31909','TM31889','TM32098','TM31962','TM31955','TM31834','TM32621','TM32595','TM32518','TM33801','TM33998','TM33791','TM33784','TM33779','TM33778','TM33344','TM33568','TM43332','TM43329','TM43326','TM43324','TM33565','TM33564','TM33560','TM33392','TM32930','TM32928','TM33400','TM33399','TM33397','TM33395','TM33184','TM34143','TM34216','TM34212','TM32881','TM32880','TM32882','TM34371','TM34366','TM34364','TM34384','TM34381','TM34380','TM34379','TM34375','TM34374','TM34373','TM34372','TM34402','TM34401','TM34400','TM34398','TM34396','TM37181','TM32710','TM32353','TM36080','TM36075','TM36072','TM36070','TM36316','TM36313','TM36059','TM36056','TM36055','TM36052','TM33613','TM34472','TM34475','TM34484','TM34479','TM34478','TM34469','TM34467','TM34466','TM34465','TM34923','TM34838','TM35140','TM35139','TM35138','TM35131','TM36837','TM36836','TM36834','TM36832','TM36830','TM36829','TM36828','TM36827','TM35129','TM35123','TM35121','TM34518','TM34532','TM36210','TM34541','TM34538','TM34537','TM34583','TM34582','TM34575','TM34573','TM34571','TM34567','TM34559','TM32935','TM32593','TM32306','TM32168','TM32162','TM32109','TM36329','TM36326','TM36322','TM36318','TM36867','TM36952','TM36949','TM37484','TM37535','TM36407','TM36405','TM36403','TM36688','TM36686','TM36117','TM36116','TM36114','TM36113','TM36112','TM37054','TM37053','TM36958','TM36955','TM36983','TM36981','TM36966','TM36965','TM36992','TM37813','TM37812','TM37810','TM37809','TM39986','TM39686','TM39696','TM39693','TM39689','TM38898','TM38896','TM38895','TM38881','TM38892','TM38891','TM37637','TM37635','TM37633','TM37631','TM39240','TM39230','TM39229','TM39227','TM39225','TM39223','TM39222','TM39216','TM39212','TM39210','TM39204','TM39201','TM39196','TM37665','TM37658','TM37656','TM37654','TM37653','TM37652','TM37651','TM37650','TM37648','TM37647','TM37646','TM37642','TM39449','TM39448','TM39445','TM39357','TM39355','TM39352','TM39351','TM39350','TM39349','TM39344','TM39342','TM39341','TM39335','TM39330','TM39325','TM39311','TM39310','TM39308','TM39306','TM39303','TM39301','TM39299','TM39298','TM39297','TM39296','TM39294','TM39292','TM39291','TM39290','TM39286','TM39285','TM39283','TM39280','TM39279','TM39275','TM39274','TM39269','TM39268','TM39267','TM39260','TM39246','TM39244','TM39242','TM42036','TM39434','TM39427','TM39425','TM39410','TM39399','TM39394','TM39181','TM39176','TM39174','TM38049','TM38047','TM38045','TM38636','TM38635','TM38632','TM38631','TM37767','TM37765','TM37771','TM37770','TM37769','TM37768','TM37762','TM38293','TM38292','TM38290','TM38286','TM38193','TM38192','TM38191','TM38190','TM38189','TM37781','TM37780','TM38834','TM38833','TM38831','TM37470','TM37469','TM37468','TM37466','TM37465','TM37463','TM37462','TM37460','TM37458','TM37457','TM37416','TM37414','TM37413','TM37412','TM37401','TM37400','TM37397','TM37286','TM37454','TM38825','TM39583','TM39577','TM38638','TM38444','TM38443','TM38427','TM38408','TM38405','TM38391','TM38385','TM38353','TM38330','TM38162','TM38161','TM38158','TM37894','TM41598','TM41348','TM41343','TM41339','TM41336','TM42419','TM42418','TM42415','TM41615','TM41614','TM41610','TM41608','TM41606','TM41605','TM41603','TM41601','TM44643','TM44640','TM44638','TM44637','TM44634','TM44633','TM44632','TM44627','TM39781','TM39776','TM39773','TM39772','TM39770','TM39768','TM39767','TM39765','TM39762','TM44662','TM44660','TM44658','TM44657','TM44655','TM44653','TM44651','TM44650','TM44649','TM44648','TM44647','TM44646','TM49788','TM49781','TM51105','TM51100','TM49142','TM49141','TM49135','TM43375','TM43477','TM43499','TM43498','TM43495','TM42772','TM42771','TM42769','TM42761','TM42757','TM43485','TM45947','TM43515','TM44595','TM44591','TM45929','TM44624','TM44612','TM44609','TM43792','TM43766','TM43781','TM43772','TM42006','TM42002','TM31536','TM31172','TM42070','TM42076','TM42072','TM43596','TM43595','TM43594','TM43592','TM43585','TM45366','TM47384','TM47383','TM47381','TM47374','TM48147','TM48141','TM46936','TM46943','TM46942','TM46941','TM46939','TM45533','TM45531','TM45548','TM45760','TM45319','TM45074','TM45073','TM45094','TM45081','TM45078','TM45076','TM45091','TM45089','TM45062','TM45071','TM49811','TM50256','TM50246','TM50244','TM50238','TM49064','TM48564','TM49375','TM50229','TM49229','TM49227','TM50025','TM49836','TM49834','TM50064','TM50056','TM50032','TM50314','TM50313','TM50311','TM50310','TM50309','TM50074','TM50073','TM50786','TM50785','TM50784','TM49765','TM49767','TM50929','TM54023','TM54019','TM54011','TM53419','TM53418','TM53035','TM53026','TM53021','TM53019','TM52307','TM54314','TM54310','TM54080','TM54075','TM54024','TM50393','TM50402','TM50400','TM50398','TM50743','TM50741','TM50739','TM50753','TM51938','TM50766','TM50765','TM52394','TM52393','TM52392','TM52391','TM52389','TM52227','TM52217','TM54037','TM54031','TM52414','TM42443','TM42433','TM40195','TM40194','TM40191','TM40212','TM40210','TM40209','TM40202','TM40201','TM41555','TM41553','TM43532','TM43530',]
def cell_changed():
    cellid = selected_cell
    
    raw_df = sql.run_query("select cellid, cycle, fade from cyclingbycycledata where cellid = '{}' and cycle > 70".format(cellid), 'db03', 'testdata')
    raw_df['fade_']= raw_df['fade']
#     raw_df['fade'] =raw_df['fade'].rolling(10).mean()
    raw_df['diff'] = abs(raw_df['fade_'] - raw_df['fade'])
    raw_df.loc[raw_df["diff"] > 0.01, 'fade'] = np.nan
    if raw_df['fade'].max() > 0.2:
        interpolate_fade(raw_df.dropna(),150)
    else:
        extrapolate_fade(raw_df,500)
    fig = extrapolate_fade(raw_df,500)
    fig1 = interpolate_fade(raw_df.dropna(),150)
    global img_string
    global img_string_int
    img_string = ''
    img_string_int = ''
    import base64
    img_bytes = fig.to_image(format="jpeg")
    img_string = base64.b64encode(img_bytes).decode('utf-8')
    img_string_int = base64.b64encode(fig1.to_image(format="jpeg")).decode('utf-8')
    ds.image(img_string)
    ds.image(img_string_int)
    
import datastack as ds
ds.write('Electrolyte explorer')
selected_cell = ds.select(cells, on_change=cell_changed)
ds.write('selected cell: ' + selected_cell)
def map_cycle():
    cells_df = pd.DataFrame({"cells":cells})
    for cell in cells_df['cells']:
        raw_df =''
        raw_df = sql.run_query("select cellid, cycle, fade from cyclingbycycledata where cellid = '{}' and cycle > 70".format(cell), 'db03', 'testdata')
        raw_df['fade_']= raw_df['fade']
        if raw_df['fade'].max() > 0.2:
            try:
                cycle = interpolate_fade(raw_df.dropna(),150, r='cycle')
            except Exception as e:
                print(e)
                cycle = 0
            cells_df.loc[cells_df["cells"] == cell, 'cycle'] = cycle
            cells_df.loc[cells_df["cells"] == cell, 'type'] = 'intra'
        else:
            try:
                cycle = extrapolate_fade(raw_df,500, r='cycle')
            except:
                cycle = 0
            cells_df.loc[cells_df["cells"] == cell, 'cycle'] = cycle
            cells_df.loc[cells_df["cells"] == cell, 'type'] = 'extra'
    return cells_df
# map_df = map_cycle()
# map_df.to_csv('map.csv')
import plotly.express as px
px.bar(map_df, x='cells', y='cycle')
px.histogram(map_df, x="cycle")
map_df[map_df['cycle']< 1]
map_df
