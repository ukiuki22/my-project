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

def sgn(x):
    if x>0 : return 1
    else: return -1


time = lambda week,day,hour,mins: 24*60*7*week+24*60*day+60*hour+mins
#前後1日の平均(1時間ごと)
ave_day = lambda week,day,hour : np.average([df.iloc[time(week,day,hour+i,0),1] for i in range(-12,12)])
Ev_day  = lambda week,day      : [df.iloc[time(week,day,i,0),1]/ave_day(week,day,i) for i in range(24)]

#前後1週間の平均(3時間ごと)
ave_week = lambda week,day,hour : np.average([df.iloc[time(week,day,hour+3*i,0),1] for i in range(-8*3,8*3)])
Ev_week  = lambda week      : [df.iloc[time(week,0,i,0),1]/ave_week(week,0,i) for i in range(24*7)]


daystime = [i/24 for i in range(24*7)]
# for j in range(3,daycount-3):
# plt.plot(daystime,Ev_week(1))
# plt.plot(Ev_week(2))
# plt.plot(Ev_week(46))

Ev_week_ave=[np.average((np.array([Ev_week(j) for j in range(1,4*12*3-1)]).T)[i]) for i in range(24*7)]
# Ev_day_ave=[np.average((np.array([Ev_day(0,j) for j in range(1,daycount-1)]).T)[i]) for i in range(24)]
# plt.plot(Ev_day_ave,'k')
print(Ev_week_ave)

plt.plot(daystime,Ev_week_ave)
plt.xlim(0,7)
plt.savefig(str(daycount)+".png")
# plt.show()
