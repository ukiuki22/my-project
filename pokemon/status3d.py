import pandas as pd
import numpy  as np
# import os
import matplotlib.pyplot as plt
# from   datetime import datetime as dt
# from   functools import reduce
# from   itertools import combinations,product
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py
offline.init_notebook_mode()


# 各ポケモンの情報を読み込み
pk  = pd.read_csv('./csv/characteristics.csv',encoding="SHIFT-JIS")

dfc = lambda num : pk.loc[num,'h']*min(pk.loc[num,'b'],pk.loc[num,'d'])/100
atk = lambda num :                 max(pk.loc[num,'a'],pk.loc[num,'c'])
spd = lambda num : pk.loc[num,'s']

dfcList = [dfc(i) for i in range(len(pk))]
atkList = [atk(i) for i in range(len(pk))]
spdList = [spd(i) for i in range(len(pk))]

trace1 = go.Scatter3d(
    x = dfcList,
    y = atkList,
    z = spdList,
    mode ='markers',
    marker=dict(
        color='rgb(0,0,256)',
        size=2,
        symbol='circle',
        line=dict(
            color='rgb(204, 204, 204)',
            width=1
        ),
        opacity=0.9
    )
)

data=[trace1]
# layout= dict(height=700, width=600)
fig= go.Figure(data=data, layout=go.Layout())
offline.plot(fig,filename='test.html')

# plt.scatter(spdList,atkList)
# plt.show()
