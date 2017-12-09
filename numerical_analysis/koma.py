import numpy as np
from scipy.integrate import odeint
import  matplotlib.pyplot as plt

import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py
offline.init_notebook_mode()

# plt.use.style('ggplot')
plt.style.use('ggplot')

i1,i2,i3 = 1,2.5,3
mu       = 0.1

track = 15
t_range = np.linspace(0,track*np.pi,track*10)

def func(omega,init):
    [w1,w2,w3]=omega
    dw1 = (i2-i3)/i1 * w2 * w3
    dw2 = (i3-i1)/i2 * w3 * w1
    dw3 = (i1-i2)/i3 * w1 * w2 - mu*w3/i3
    return [dw1,dw2,dw3]

# if __name__ == '__main__':
output = odeint(func,[0.1,0,1],t_range)
w1 = output[:,0]
w2 = output[:,1]
w3 = output[:,2]
w  = np.sqrt(w1**2+w2**2+w3**2)
l1 = i1*w1
l2 = i2*w2
l3 = i3*w3
l  = np.sqrt(l1**2+l2**2+l3**2)


# plotly
trace1 = go.Scatter3d(
    x = l1/l,
    y = l2/l,
    z = l3/l,
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

trace2 = go.Scatter3d(
    x = w1/w,
    y = w2/w,
    z = w3/w,
    mode ='markers',
    marker=dict(
        color='rgb(0,256,0)',
        size=2,
        symbol='circle',
        line=dict(
            color='rgb(204, 204, 204)',
            width=1
        ),
        opacity=0.9
    )
)

data=[trace1,trace2]
fig= go.Figure(data=data, layout=go.Layout())
offline.plot(fig,filename='test.html')



plt.plot(t_range/np.pi,output[:,0])
plt.plot(t_range/np.pi,output[:,1])
plt.plot(t_range/np.pi,output[:,2])
# plt.show() 

# fig = plt.figure()
# ax1 = fig.add_subplot(211)
# ax2 = fig.add_subplot(212,sharex=ax1)
# ax1 = fig.add_axes((0, 0.8, 1, 0.2))
# ax2 = fig.add_axes((0, 0, 1, 0.8), sharex=ax1)

#横から見る
# plt.figure(figsize=(6,3))
# plt.xlim(-1,1)
# plt.ylim(0.7,1)
# ax1.plot(w1/w,w3/w)
# ax1.plot(l1/l,l3/l)
# plt.plot(w1/w,w3/w)
# plt.plot(l1/l,l3/l)

# 上から見る
# plt.figure(figsize=(6,6))
# plt.xlim(-1,1)
# plt.ylim(-1,1)
# ax2.plot(w1/w,w2/w)
# ax2.plot(l1/l,l2/l)
# plt.plot(w1/w,w2/w)
# plt.plot(l1/l,l2/l)


# plt.show()
