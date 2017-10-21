import numpy as np
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py
offline.init_notebook_mode()

t = np.arange(0,10,0.1)

trace1 = go.Scatter3d(
    x = np.sin(3*t)*np.exp(-t/5),
    y = np.cos(3*t)*np.exp(-t/5),
    z = np.exp(-t/5),
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
