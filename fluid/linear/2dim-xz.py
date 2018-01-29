# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

"""
xz平面　--内部重力波を起こす--
"""

x_max,z_max = 100,100
nX ,nZ = 10,10
dx,dz = x_max/nX , z_max/nZ
dt,nT =  0.1 ,10 #sec

rho0 = 1
g    = 1
H    = 10


x = np.linspace(-nX*dx/2,nX*dx/2,nX)
z = np.linspace(0,nZ*dz,nZ)

x2 = np.linspace(-(nX/2+1)*dx,(nX/2+1)*dx,nX+2)
z2 = np.linspace(-1*dz,(nZ+1)*dz,nZ+2)

# u,rho,dPx,w
def initCondition() :

    init_u = lambda i,j: max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,0)
    init_r = lambda i,j: 0.01 * max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,0)
    init_w = lambda i,j: -max(np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx) )-0.5 ,0)
    init_P = lambda i,j: np.sin(2*np.pi* ((i+j)*dx) / (2*nX*dx)) #微分して用いる量なので，境界部分の計算も入れておく必要がある

    u,r,P,w = np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2]), np.zeros([nX+2, nZ+2])

    for i in range(nX):
        for j in range(nZ):
            u[i+1][j+1]   = init_u(i,j)
            r[i+1][j+1]   = init_r(i,j)
            w[i+1][j+1]   = init_w(i,j)

    for i in range(nX+2):
        for j in range(nZ+2):
            P[i][j] = init_P(i,j)

    return (u,r,P,w)


def step(field) :
    (u,r,P,w) = field

    dPx = lambda i,j: (P[i+1][j] - P[i][j])/dx

    update_u = lambda i,j : u[i][j] +  dPx(i,j) /rho0        * dt
    update_r = lambda i,j : r[i][j] -  rho0/H * w[i][j]      * dt

    upper_p = lambda i,j : P[i][j] - g * rho[i][j] * dz
    upper_w = lambda i,j : w[i][j] - (u[i+1][j]-u[i][j])/dx * dz

    next_u,next_r = np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2])

    for i in range(1,nX+1):
        for j in range(1,nZ+1):
            next_u[i][j] = update_u(i,j)
            next_r[i][j] = update_r(i,j)

    return (next_u,next_r,P,w)

nowtime = datetime.now().strftime('%m%d_%H%M%S')
number = 0
os.mkdir('./'+nowtime+'s')
os.mkdir('./'+nowtime+'v')
field = initCondition()
U0, Rho0, P0, W0= field

loop = 10
for i in range(loop):
    U, Rho, P, W= field
    if 10*i%loop == 0 :
        X, Z = np.meshgrid(x2,z2)
        M = np.array([[np.sqrt(U[i][j]**2+W[i][j]**2) for j in range(nX+2)] for i in range(nZ+2)])

        plt.quiver( X, Z, U, W, M, units='x', pivot='mid',scale=0.1)
        plt.savefig('./'+nowtime+'v/'+"%03.f"%(number))
        # plt.show()
        plt.clf()
        number +=1

    # if 5*i%loop == 0 :
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     im = ax.imshow(Rho, interpolation='none')
    #     fig.colorbar(im)
    #     # plt.quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)
    #     plt.savefig('./'+nowtime+'s/'+"%03.f"%(number))
    #     number += 1
    #     plt.clf()

    new_field = step(field)
    field = new_field

# print(U-U0)
# print(Rho-Rho0)
# plt.show()
