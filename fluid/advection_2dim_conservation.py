# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

fig = plt.figure()
ims = []


"""
風上差分で2次元移流方程式を解く
"""

dx,nX =  1.00 ,10 #m
dy,nY =  1.00 ,10 #m
dt,nT =  0.01 ,10 #sec
c = 10 #m/s

x = np.linspace(0,nX*dx,nX)
y = np.linspace(0,nY*dy,nY)

x2 = np.linspace(-dx,(nX+1)*dx,nX+2)
y2 = np.linspace(-dy,(nY+1)*dy,nY+2)

def initCondition() :
    init_u = lambda i,j: max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,0)
    init_v = lambda i,j: max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,0)

    u,v = np.zeros([nX+2, nY+2]) , np.zeros([nX+2, nY+2])

    for i in range(nX):
        for j in range(nY):
            u[i+1][j+1] = init_u(i,j)
            v[i+1][j+1] = init_v(i,j)

    return (u,v)


def step(field) :
    (u,v) = field
    f = lambda u,i,j: c * u[i][j]

    f_foward = lambda u,i,j : 0.5 * ( ( f(u,i+1,j)+ f(u,i  ,j) ) - abs(c) * (u[i+1][j]-u[i][j]  ) )
    f_back   = lambda u,i,j : 0.5 * ( ( f(u,i  ,j)+ f(u,i-1,j) ) - abs(c) * (u[i][j]  -u[i-1][j]) )
    g_foward = lambda u,i,j : 0.5 * ( ( f(u,i,j+1)+ f(u,i,j  ) ) - abs(c) * (u[i][j+1]-u[i][j]  ) )
    g_back   = lambda u,i,j : 0.5 * ( ( f(u,i  ,j)+ f(u,i,j-1) ) - abs(c) * (u[i][j]  -u[i][j-1]) )

    update = lambda u,i,j : u[i][j] -  (dt/dx) * (f_foward(u,i,j) - f_back(u,i,j)) \
                                    -  (dt/dy) * (g_foward(u,i,j) - g_back(u,i,j))

    next_u,next_v = np.zeros([nX+2, nY+2]) , np.zeros([nX+2, nY+2])

    periodicX2 = lambda next_u,i : next_u[i][-2]
    periodicY2 = lambda next_u,j : next_u[-2][j]
    periodicX1 = lambda next_u,i : next_u[i][1]
    periodicY1 = lambda next_u,j : next_u[1][j]

    for i in range(1,nX+1):
        for j in range(1,nY+1):
            next_u[i][j] = update(u,i,j)
            next_v[i][j] = update(v,i,j)
# TODO:
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

    return (next_u,next_v)

nowtime = datetime.now().strftime('%m%d_%H%M%S')
os.mkdir('./'+nowtime)
field = initCondition()
for i in range(50):
    X, Y = np.meshgrid(x2,y2)
    U, V = field
    # U, V = initCondition()
    M = np.array([[np.sqrt(U[i][j]**2+V[i][j]**2) for j in range(nX+2)] for i in range(nY+2)])

    plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)
    plt.savefig('./'+nowtime+'/'+"%03.f"%(i))
    plt.clf()

    new_field = step(field)
    field = new_field

plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)

plt.show()

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
