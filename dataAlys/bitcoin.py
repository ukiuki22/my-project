import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
plt.style.use('ggplot')
# Data Source : https://www.kaggle.com/mczielinski/bitcoin-historical-data/data
"""
その日だけのデータで規格化すると上がりトレンドだった場合に，上がり調子になる（両端で連続してない）
ただしその日の終値よりも高ければよしという戦略だったらその日だけのデータでも大丈夫
"""

alldays = 7*4*12
# test2 N日分(00:00-23:59)
read_first= lambda n:int(-9*60-1-24*60*n)
read_last = int(-9*60-1)

# df_mega = pd.read_csv('/Users/***/my-project/bitcoin/coincheckJPY_1-min_data_2014-10-31_to_2018-01-08.csv')
# df_mega.iloc[read_first(alldays):read_last,0:2].to_csv('./'+str(alldays)+'days.csv')


df = pd.read_csv('./'+str(alldays)+'days.csv',
                 parse_dates=[1],
                 date_parser=lambda x: str(datetime.fromtimestamp(float(x))) )
del df['Unnamed: 0']

#データを日にちごとに分割
def parDays(df,day):
    time,price=[],[]
    for i in range(60*24):
        time  += [i/60] #時間
        price += [df.iloc[i+60*24*day,1]]
    def sgn(x):
        if x>0 : return 1
        else: return -1
    # 平均からのズレ（偏差）
    # diff = [1000*price[i]/np.average(price)-1000  for i in range(len(price))]
    # 06:00からのズレ
    # diff = [1000*price[i]/price[-1]-1000  for i in range(len(price))]
    # （始値＋終値）／2からのズレ
    # diff = [1000*2*price[i]/(price[0]+price[-1])-1000  for i in range(len(price))]
    # その日の終値との差を比較
    # diff = [(price[i]/price[-1]-1)*1000 for i in range(len(price))]
    # その日の終値より高くなるか低くなるか
    # diff = [sgn(price[i]/price[-1]-1) for i in range(len(price))]
    # 平均よりも高くなるかどうか
    diff = [sgn(price[i]/np.average(price)-1)  for i in range(len(price))]
    return(time,diff,df.iloc[60*24*day,0])


diffs = []
for j in range(alldays):
    (time,diff,date) = parDays(df,j)
    diffs += [diff]
    plt.plot(time,diff)
plt.savefig('1.png')
#ある時刻での偏差の平均
ave1day = [np.average(np.array(diffs).T[j]) for j in range(60*24)]

    # print(diffs[j][1])
plt.clf()
plt.title('until '+str(date)+' over '+str(alldays)+' days')
plt.xlim(0,24)
plt.plot(time,ave1day,'k')
plt.savefig('3.png')
plt.show()
# print(time)

# y = df['Open']
# x = df['Timestamp']
# plt.plot(x,y)
# plt.show()
