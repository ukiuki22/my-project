# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

fig = plt.figure()
ims = []


"""
線形化したオイラー方程式（コリオリ力／圧力勾配力実装）
非線形にしないと何も面白くなさそう
"""

x_max,y_max = 100,100
nX ,nY = 10,10
dx,dy = x_max/nX , y_max/nY
dt,nT =  0.1 ,10 #sec
f = 1 #1/sec コリオリパラメーター
rho0 = 1

x = np.linspace(-nX*dx/2,nX*dx/2,nX)
y = np.linspace(-nY*dy/2,nY*dy/2,nY)

x2 = np.linspace(-(nX/2+1)*dx,(nX/2+1)*dx,nX+2)
y2 = np.linspace(-(nY/2+1)*dy,(nY/2+1)*dy,nY+2)

def initCondition() :


    init_u = lambda i,j: max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,-1)
    init_v = lambda i,j: max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,-1)
    init_P = lambda i,j: i*dx #微分して用いる量なので，境界部分の計算も入れておく必要がある

    init_Px = lambda i,j: (init_P(i+1,j) - init_P(i,j))/dx
    init_Py = lambda i,j: (init_P(i,j+1) - init_P(i,j))/dx

    u,v,dPx,dPy = np.zeros([nX+2, nY+2]) , np.zeros([nX+2, nY+2]) , np.zeros([nX+2, nY+2]), np.zeros([nX+2, nY+2])

    for i in range(nX):
        for j in range(nY):
            u[i+1][j+1] = init_u(i,j)
            v[i+1][j+1] = init_v(i,j)
            dPx[i+1][j+1] = init_Px(i,j)
            dPy[i+1][j+1] = init_Py(i,j)

    return (u,v,dPx,dPy)


def step(field) :
    (u,v,dPx,dPy) = field
    # TODO: 1dimバーガーズから保存形式を持ってくる　＆　そこになかった項を移流方程式みたいにc＝vでついか
    # # f = lambda u,i,j: c * u[i][j]
    # #
    # f_foward = lambda u,v,i,j : 0.5 * ( ( f(u,i+1,j)+ f(u,i  ,j) ) - abs(c) * (u[i+1][j]-u[i][j]  ) )
    # f_back   = lambda u,v,i,j : 0.5 * ( ( f(u,i  ,j)+ f(u,i-1,j) ) - abs(c) * (u[i][j]  -u[i-1][j]) )
    # g_foward = lambda u,v,i,j : 0.5 * ( ( f(u,i,j+1)+ f(u,i,j  ) ) - abs(c) * (u[i][j+1]-u[i][j]  ) )
    # g_back   = lambda u,v,i,j : 0.5 * ( ( f(u,i  ,j)+ f(u,i,j-1) ) - abs(c) * (u[i][j]  -u[i][j-1]) )

    update_u = lambda i,j : u[i][j] + f * v[i][j] * dPx[i][j] /rho0 * dt
    update_v = lambda i,j : v[i][j] - f * u[i][j] * dPy[i][j] /rho0 * dt

    next_u,next_v = np.zeros([nX+2, nY+2]) , np.zeros([nX+2, nY+2])

    for i in range(1,nX+1):
        for j in range(1,nY+1):
            next_u[i][j] = update_u(i,j)
            next_v[i][j] = update_v(i,j)
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

    return (next_u,next_v,dPx,dPy)

nowtime = datetime.now().strftime('%m%d_%H%M%S')
number = 0
os.mkdir('./'+nowtime)
field = initCondition()

loop = 10
for i in range(loop):

    if 10*i%loop == 0 :
        X, Y = np.meshgrid(x2,y2)
        U, V ,px,py= field
        # U, V = initCondition()
        M = np.array([[np.sqrt(U[i][j]**2+V[i][j]**2) for j in range(nX+2)] for i in range(nY+2)])

        plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)
        plt.savefig('./'+nowtime+'/'+"%03.f"%(number))
        plt.clf()
        number +=1

    new_field = step(field)
    field = new_field

plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=0.1)

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
