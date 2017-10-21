# source: http://www.mathgram.xyz/entry/plotly
# 必要最低限

import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode()

from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
#
# iris = load_iris()
# columns = iris.feature_names
#
# make dataframe
# df = pd.DataFrame(iris.data, columns=columns)

# make trace
trace = go.Scatter(
    x = np.array([0,0,1,1,2,2]), #df[columns[0]]
    y = np.array([1,2,3,4,5,6]),  #df[columns[1]]
    mode = "markers")

# define layout
layout = go.Layout()
    # title='Iris sepal length-width',
    # xaxis=dict(title='sepal legth(cm)'),
    # yaxis=dict(title='sepal width(cm)'),
    # showlegend=False)

# data = [trace]
fig = dict(data=[trace], layout=layout)

offline.plot(fig) #, filename="Iris-sample-scatter", image="png")
