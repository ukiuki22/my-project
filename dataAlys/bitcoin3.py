import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import math as math
plt.style.use('ggplot')

daycount = 7*4*12*3
df = pd.read_csv('./'+str(daycount)+'days.csv',
                 parse_dates=[1],
                 date_parser=lambda x: str(datetime.fromtimestamp(float(x))) )
del df['Unnamed: 0']

time = lambda week,day,hour,mins: 24*60*7*week+24*60*day+60*hour+mins
#前後1日の平均(1時間ごと)
ave_day = lambda week,day,hour : np.average([df.iloc[time(week,day,hour+i,0),1] for i in range(-12,12)])
Ev_day  = lambda week,day      : [df.iloc[time(week,day,i,0),1]/ave_day(week,day,i) for i in range(24)]

#前後1週間の平均(3時間ごと)
ave_week = lambda week,day,hour : np.average([df.iloc[time(week,day,hour+3*i,0),1] for i in range(-8*3,8*3)])
Ev_week  = lambda week      : [df.iloc[time(week,0,i,0),1]/ave_week(week,0,i) for i in range(24*7)]


daystime = [i/24 for i in range(24*7)]


#全ての時間の評価関数のリストを返す
# a = [Ev_week(j) for j in range(1,4*12*3-1)]
# print(a)
#
# df2 = pd.DataFrame(a)
# df2.to_csv('ev1008.csv',index=None)

#評価関数の値の加工
df3 = pd.read_csv('ev1008.csv')
# df3 = pd.read_csv('aaa.csv')
# datalist = [list(df3.loc[j]) for j in range(3)]
datalist = [list(df3.loc[j]) for j in range(4*12*3-2)]

# 1. 滑らかにする
smooth = lambda n,data : data[:n]+[ sum(data[i-n:i+n+1])/(2*n+1) for i in range(n,len(data)-n)] + data[-n:]

s1 = [smooth(2,smooth(2,smooth(1,datalist[j]))) for j in range(len(datalist))]

# 2. 平均を取って滑らか/滑らかにして平均
# s2 = [np.average(np.array(s1).T[j]) for j in range(24*7)]
s2 = smooth(2,smooth(2,smooth(1,[np.average(np.array(datalist).T[j]) for j in range(24*7)])))

# 3. 標準偏差
# s3 = smooth(2,smooth(2,smooth(1,[np.std(np.array(datalist).T[j]) for j in range(24*7)])))
s3 = [np.std(np.array(s1).T[j]) for j in range(24*7)]

# 4. エラーバー的なもの
s4p = [s2[i]+0.1*s3[i] for i in range(24*7)]
s4m = [s2[i]-0.1*s3[i] for i in range(24*7)]

# for j in range(len(datalist)):
#     plt.plot(daystime,s1[j],'b')#,alpha=0.1)

plt.plot(daystime,s2)
plt.plot(daystime,[s3[i]-np.average(s3)+1 for i in range(24*7)])
# plt.plot(daystime,s4p,alpha=0.6)
# plt.plot(daystime,s4m,alpha=0.6)
# plt.show()

plt.xlim(0,7)
# plt.ylim(0.99,1.01)
nowtime = datetime.now().strftime('%m%d_%H%M%S')
plt.savefig(str(nowtime)+".png")

# Ev_week_ave=[np.average((np.array([Ev_week(j) for j in range(1,4*12*3-1)]).T)[i]) for i in range(24*7)]
# # Ev_day_ave=[np.average((np.array([Ev_day(0,j) for j in range(1,daycount-1)]).T)[i]) for i in range(24)]
# # plt.plot(Ev_day_ave,'k')
# print(Ev_week_ave)
#
# plt.plot(daystime,Ev_week_ave)
# plt.xlim(0,7)
# plt.savefig(str(daycount)+".png")
# # plt.show()
