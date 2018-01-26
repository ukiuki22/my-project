import numpy as np
import  matplotlib.pyplot as plt
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
# 水の表面張力
gamma = 0.073 #J/m2
# 水の密度
rho_l = 1000 #kg/m3
# non-dimentional
eps = 0.622
kap = R_d/c_p
# term1 = L0/(c_p*T0)
# term3 = es0/P0

#計算範囲　200K~300K 100hPa~1000hPa
set_p = np.linspace(1000/P0,500/P0,100)
set_t = np.linspace(300/T0,250/T0,100)
set_T = np.linspace(300,250,100)
set_RH = np.linspace(1.0,1.1,100)
set_a  = np.array([10**idx for idx in np.linspace(-8,-5,100)])

# 飽和水蒸気圧
# term2 = L0/(R_d*T0)
es = lambda T : es0*np.exp(L0/R_d*(1/T0-1/T))
set_es = np.array([es(T) for T in set_T])

# Gibbs p43
alpha = 4*np.pi*gamma
beta  = lambda T,RH :4/3*np.pi*rho_l*R_v* T *np.log(RH)
termA = lambda T    : 2*gamma/(rho_l*R_v* T)
gibbs = lambda RH,a,T : -beta(T,RH)*a**3 + alpha*a**2
set_gibbs = np.array([[gibbs(RH,a,270) for a in set_a] for RH in set_RH])
# Kelvin's formula p44
kelvin = lambda T,a : es(T)*np.exp(termA(T)/a)

set_RH_droplet = np.array([[np.exp(termA(T)/a) for a in set_a] for T in set_T])
# plt.plot(set_a,set_RHdroplet)

# set_gibbs = lambda RH :np.array([gibbs(RH,2*a*1e-10,300) for a in range(1,100)])
# plt.plot(set_gibbs(1.1))

# plt.plot(T0*set_t-273,set_es)
plt.xscale("log")
RH_map,a_map = np.meshgrid(set_RH,set_a)
plt.contour(a_map, 100*RH_map, set_gibbs, 8, alpha=.75) #,levels=templevels) #, cmap=plt.cm.hot)
plt.show()
