# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ims = []


"""
風上差分で1次元移流方程式を解く/保存形式に書き換え
"""

dx,nX =  1.00 ,100 #m
dt,nT =  0.01 ,120 #sec
c = 100 #m/s

x = np.linspace(0,nX*dx,nX)
# t = np.linspace(0,nT*dt,nT)

# initCondition = [1 for i in range(int(0.25*nX))] + [0 for i in range(int(0.75*nX))]
initCondition = [np.sin(2*np.pi*x/(0.5*nX*dx))[i] for i in range(int(0.5*nX))] + [0 for i in range(int(0.5*nX))]

def step(u) :
    f = lambda u,j: c * u[j]
    f_foward = lambda u,j : 0.5 * ( ( f(u,j+1)+ f(u,j) ) - abs(c) * (u[j+1]-u[j]) )
    f_back   = lambda u,j : 0.5 * ( ( f(u,j)+ f(u,j-1) ) - abs(c) * (u[j]-u[j-1]) )
    func = lambda u,j : u[j] -     (dt/dx) * (f_foward(u,j) - f_back(u,j))

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
        im = plt.plot(u,label=str(i*dt)+' sec')
        ims.append(im)

    u_next = step(u)
    u      = u_next


# print(u)
# plt.legend()
plt.show()
