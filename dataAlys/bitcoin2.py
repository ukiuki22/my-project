import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
plt.style.use('ggplot')

daycount = 7*4*12
df = pd.read_csv('./'+str(daycount)+'days.csv',
                 parse_dates=[1],
                 date_parser=lambda x: str(datetime.fromtimestamp(float(x))) )
del df['Unnamed: 0']

def sgn(x):
    if x>0 : return 1
    else: return -1


time = lambda week,day,hour,mins: 24*60*7*week+24*60*day+60*hour+mins
#前後1日の平均(1時間ごと)
ave_day = lambda week,day,hour : np.average([df.iloc[time(week,day,hour+i,0),1] for i in range(-12,12)])
Ev_day  = lambda week,day      : [df.iloc[time(week,day,i,0),1]/ave_day(week,day,i) for i in range(24)]

# for j in range(1,daycount-1):
#     plt.plot(Ev_day(0,j))

Ev_day_ave=[np.average((np.array([Ev_day(0,j) for j in range(1,daycount-1)]).T)[i]) for i in range(24)]
plt.plot(Ev_day_ave,'k')
plt.show()


# #データを日にちごとに分割
# def parDays(df,day):
#     time,price=[],[]
#     for i in range(60*24):
#         time  += [i/60] #時間
#         price += [df.iloc[i+60*24*day,1]]
#     # 平均からのズレ（偏差）
#     # diff = [1000*price[i]/np.average(price)-1000  for i in range(len(price))]
#     # 06:00からのズレ
#     # diff = [1000*price[i]/price[-1]-1000  for i in range(len(price))]
#     # （始値＋終値）／2からのズレ
#     # diff = [1000*2*price[i]/(price[0]+price[-1])-1000  for i in range(len(price))]
#     # その日の終値との差を比較
#     # diff = [(price[i]/price[-1]-1)*1000 for i in range(len(price))]
#     # その日の終値より高くなるか低くなるか
#     # diff = [sgn(price[i]/price[-1]-1) for i in range(len(price))]
#     # 平均よりも高くなるかどうか
#     diff = [sgn(price[i]/np.average(price)-1)  for i in range(len(price))]
#     return(time,diff,df.iloc[60*24*day,0])
#
# #その日はどれくらい/どっちに変化した？
# def parDays2(df,day):
#         begin = df.iloc[60*24*day,1]
#         end   = df.iloc[60*24*(day+1)-1,1]
#         return (sgn(end/begin-1),df.iloc[60*24*day,0])
#
# dayOfTheWeek = [[] for i in range(7)]
# for j in range(daycount):
#     (diff,date) = parDays2(df,j)
#     print(diff,date)
#     #2018-01-01は月曜だからdaycountが7の倍数なら丁度月曜始まり
#     dayOfTheWeek[j%7] += [diff]
# # print(dayOfTheWeek)
#
# aveDay = [np.average(dayOfTheWeek[i]) for i in range(7)]
# print(aveDay)
# plt.bar([0,1,2,3,4,5,6],aveDay)
# plt.show()
#
"""
diffs = []
for j in range(daycount):
    (time,diff,date) = parDays(df,j)
    diffs += [diff]
    # plt.plot(time,diff)
# plt.savefig('1.png')
#ある時刻での偏差の平均
ave1day = [np.average(np.array(diffs).T[j]) for j in range(60*24)]
    # print(diffs[j][1])
plt.clf()
plt.title('until '+str(date)+' over '+str(daycount)+' days')
plt.xlim(0,24)
plt.plot(time,ave1day,'k')
plt.savefig('until'+str(date)+'over'+str(daycount)+'days.png')
plt.show()
"""
