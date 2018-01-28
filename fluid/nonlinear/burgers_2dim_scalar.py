# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

# fig = plt.figure()
# ims = []


"""
風上差分で2次元バーガーズ方程式を解く＠スカラー
まだ何も変更していない
とりあえずcx->u,rho->uと非線形化しても安定するかみてみる．
安定してたらcy->vにしてうまくいったらベクトルで実装．
"""

x_max,y_max = 100,100
nX ,nY = 100,100
dx,dy = x_max/nX , y_max/nY
dt,nT =  0.01 ,10 #sec
c = 10 #m/s

x = np.linspace(-nX*dx/2,nX*dx/2,nX)
y = np.linspace(-nY*dy/2,nY*dy/2,nY)

x2 = np.linspace(-(nX/2+1)*dx,(nX/2+1)*dx,nX+2)
y2 = np.linspace(-(nY/2+1)*dy,(nY/2+1)*dy,nY+2)

#流れ場
def background():
    cx,cy = np.zeros([nX+2, nY+2]) , np.zeros([nX+2, nY+2])

    r = lambda i,j : max(np.sqrt( (i*dx-nX*dx/2)**2 + (j*dy-nY*dy/2)**2 ),0.1)
    omega = 1

    for i in range(nX):
        for j in range(nY):
            cx[i+1][j+1] =   omega  * (j*dy-nY*dy/2) #* 10**2 / r(i,j)**2
            cy[i+1][j+1] = - omega  * (i*dx-nX*dx/2) #* 10**2 / r(i,j)**2

    return (cx,cy)

# X, Y = np.meshgrid(x2,y2)
# U, V = background()
#
# M = np.array([[np.sqrt(U[i][j]**2+V[i][j]**2) for j in range(nX+2)] for i in range(nY+2)])
#
# plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=10)
# plt.show()
# plt.clf()

# 初期の密度場
def initCondition() :
    rho0,k = 1,dx*nX/10
    init_rho = lambda i,j: rho0 * np.exp( -1/k**2 * ((i*dx-3*nX*dx/4)**2+(j*dy-nY*dy/2)**2))
    def init_rho2(i,j) : #棒
        if (i< (3*nX/4 +10) and i> (3*nX/4 -10)and j>(nY/2-2) and j<(nY/2+2)) : return rho0
        else: return 0

    rho = np.zeros([nX+2, nY+2])

    for i in range(nX):
        for j in range(nY):
            rho[i+1][j+1] = init_rho2(j,i)

    return rho

# plt.plot(initCondition()[50])
# plt.imshow(initCondition())
# plt.show()

def step(field) :
    rho = field
    cx,cy = background()

    f = lambda u,c,i,j: c[i][j] * u[i][j]

    f_foward = lambda u,c,i,j : 0.5 * ( ( f(u,c,i+1,j)+ f(u,c,i  ,j) ) - abs(c[i][j]) * (u[i+1][j]-u[i][j]  ) )
    f_back   = lambda u,c,i,j : 0.5 * ( ( f(u,c,i  ,j)+ f(u,c,i-1,j) ) - abs(c[i][j]) * (u[i][j]  -u[i-1][j]) )
    g_foward = lambda u,c,i,j : 0.5 * ( ( f(u,c,i,j+1)+ f(u,c,i,j  ) ) - abs(c[i][j]) * (u[i][j+1]-u[i][j]  ) )
    g_back   = lambda u,c,i,j : 0.5 * ( ( f(u,c,i  ,j)+ f(u,c,i,j-1) ) - abs(c[i][j]) * (u[i][j]  -u[i][j-1]) )

    update = lambda u,cx,cy,i,j : u[i][j] -  (dt/dx) * (f_foward(u,cx,i,j) - f_back(u,cx,i,j)) \
                                          -  (dt/dy) * (g_foward(u,cy,i,j) - g_back(u,cy,i,j))

    next_rho = np.zeros([nX+2, nY+2])

    # periodicX2 = lambda next_u,i : next_u[i][-2]
    # periodicY2 = lambda next_u,j : next_u[-2][j]
    # periodicX1 = lambda next_u,i : next_u[i][1]
    # periodicY1 = lambda next_u,j : next_u[1][j]

    for i in range(1,nX+1):
        for j in range(1,nY+1):
            next_rho[i][j] = update(rho,cx,cy,i,j)
            # next_v[i][j] = update(v,i,j)

    # for i in range(nX):
    #     next_u[i][0]   =periodicX2(next_u,i)
    #     next_v[i][0]   =periodicX2(next_v,i)
    #     next_u[i][-1]  =periodicX1(next_u,i)
    #     next_v[i][-1]  =periodicX1(next_v,i)
    #
    # for j in range(nY):
    #     next_u[0][j]   =periodicY2(next_u,j)
    #     next_v[0][j]   =periodicY2(next_v,j)
    #     next_u[-1][j] =periodicY1(next_u,j)
    #     next_v[-1][j] =periodicY1(next_v,j)

    return next_rho

nowtime = datetime.now().strftime('%m%d_%H%M%S')
number = 1
os.mkdir('./'+nowtime)
field = initCondition()

loop = 400
for i in range(loop):
    # X, Y = np.meshgrid(x2,y2)
    # U, V = field
    # # U, V = initCondition()
    # M = np.array([[np.sqrt(U[i][j]**2+V[i][j]**2) for j in range(nX+2)] for i in range(nY+2)])

    if 100*i%loop == 0 :
        plt.imshow(field)
        # plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)
        plt.savefig('./'+nowtime+'/'+"%03.f"%(number))
        number += 1
        plt.clf()

    new_field = step(field)
    field = new_field

# plt.imshow(field)
# plt.show()

#
# plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)
#
# plt.show()

# #境界のためのダミーを両端に加える
# u = [0] + initCondition + [0]
#
# res = []
# for i in range(nT):
#     if (i%40==0):
#         # res += [u[1:-1]]
#         im = plt.plot(u,label=str(i*dt)+' sec')
#         ims.append(im)
#
#     u_next = step(u)
#     u      = u_next
#
#
# # print(u)
# # plt.legend()
# plt.show()
