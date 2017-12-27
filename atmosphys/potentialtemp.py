import numpy as np
import  matplotlib.pyplot as plt

import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py
offline.init_notebook_mode()

plt.style.use('ggplot')

# 基準
T0 =  300
P0 = 1000
es0=   31.6  #300Kでの飽和水蒸気圧
# 比熱
R_d =  287
R_v =  461
c_p = 1005
# 潜熱(0度の値で代用)
L0  = 2.5*1e6
# non-dimentional
eps = 0.622
kap = R_d/c_p
term1 = L0/(c_p*T0)
term2 = L0/(R_d*T0)
term3 = es0/P0
# print(kap,term1,term2,term3)

#計算範囲　200K~300K 100hPa~1000hPa
set_p = np.linspace(1000/P0,500/P0,100)
set_t = np.linspace(300/T0,250/T0,100)


# 質量混合比
mu = lambda p,t : eps*term3*(1/p)*np.exp(term2*(1-1/t))
mu_map = np.array([[mu(p,t) for p in set_p] for t in set_t])
# 温位
PT = lambda p,t : t*p**(-kap)
PT_map = np.array([[PT(p,t) for p in set_p] for t in set_t])
# 相当温位
ePT = lambda p,t : PT(p,t)*np.exp(term1*(1/t)* mu(p,t))
ePT_map = np.array([[ePT(p,t) for p in set_p] for t in set_t])

p_map,t_map = np.meshgrid(set_p,set_t)

# 温度T,圧力Pの空気塊を1000hPaまで持って来た/基準の300Kは単に飽和水蒸気圧の基準（clacla解く時の積分定数）
plt.xlabel('Pressure')
plt.ylabel('Temperature')

Z1,Z2 = T0*ePT_map-273 , T0*PT_map-273
templevels = [20*i for i in range(-2,6)]
plt.contourf(P0*p_map, T0*t_map-273, Z1, 8, alpha=.75,levels=templevels) #, cmap=plt.cm.hot)
C = plt.contour(P0*p_map, T0*t_map-273, Z1, 8, colors='black', linewidth=.5,levels=templevels)
D = plt.contour(P0*p_map, T0*t_map-273, Z2, 8, colors='blue', linewidth=.5,levels=templevels)
plt.clabel(C, inline=1, fontsize=10)
plt.clabel(D, inline=1, fontsize=10)
plt.show()

# mu_p0 = lambda t : mu(1,t)
# plt.plot(set_t,list(map(mu_p0,set_t)))
# plt.show()
