# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt

"""
風上差分で1次元移流方程式を解く
"""

dx,nX =  1.00 ,100 #m
dt,nT =  0.01 ,120 #sec
c = 100 #m/s

x = np.linspace(0,nX*dx,nX)
# t = np.linspace(0,nT*dt,nT)

# initCondition = [1 for i in range(int(0.25*nX))] + [0 for i in range(int(0.75*nX))]
initCondition = [max(np.sin(2*np.pi*x/(nX*dx))[i],0) for i in range(nX)]

def step(u) :
    func = lambda u,j : u[j] - c * (dt/dx) * (u[j] - u[j-1])
    #境界ダミー以外の部分を計算．実データの範囲は[1,nX-1]（端っこもダミーデータのおかげで計算可能）
    next_u = [0] + [ func(u,j) for j in range(1,nX-1)] + [0]
    #境界条件
    next_u[ 0  ] = next_u[nX-2]
    next_u[nX-1] = next_u[   1]
    return next_u

#境界のためのダミーを両端に加える
u = [0] + initCondition + [0]

res = []
for i in range(nT):
    if (i%40==0):
        # res += [u[1:-1]]
        plt.plot(u,label=str(i*dt)+' sec')

    u_next = step(u)
    u      = u_next


# print(u)
plt.legend()
plt.show()
