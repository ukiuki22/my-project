# グラフ化に必要なものの準備
import matplotlib
import matplotlib.pyplot as plt

# データの扱いに必要なライブラリpy
import pandas as pd
import numpy as np
import datetime as dt

plt.style.use('ggplot')
#font = {'family' : 'meiryo'}
#matplotlib.rc('font', **font)


data = pd.read_csv('pokemon_status.csv',encoding="SHIFT-JIS")


values = ['HP', 'a', 'd', 'sa', 'sd', 's', 'sum']
xy = 821

data.plot(kind='hist',y=values[:-1],bins=50, alpha=0.5)
plt.show()



"""
#--Exsamples--#
xy_data = data.ix[:xy,['name',values[-1]]]
print(data.ix[810:815,:])

#特定の行のみ
print(data.ix[10,:])
print(data.query("name == 'イーブイ'"))

#strength = data.sort('sum')
#print(strength.ix[10,'sum'])

umple1 = data.ix[:15,["name","a","sa"]]

data.plot(kind='hexbin',x='a',y='s',gridsize=20) #,s='HP') #,cmap='cool')
print(sumple1)
sumple1.plot.bar(y=['a','sa'])
plt.show()

data.plot(kind='scatter',x='sd',y='s',s=(data['sum']/60)**2,c='HP',cmap='cool')
plt.xlim(0,200)
plt.ylim(0,200)

"""
