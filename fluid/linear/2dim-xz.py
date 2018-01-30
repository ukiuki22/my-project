# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os

"""
xz平面　--内部重力波を起こす--
"""

x_max,z_max = 20*1e3,10*1e3 #m
nX ,nZ = 100,50
dx,dz = x_max/nX , z_max/nZ
dt,nT =  10 ,10 #sec

rho0 = 1  #kg/m3
g    = 10 #m/s2
Nb   = 1e-2 #/s



x = np.linspace(0,nX*dx,nX)
z = np.linspace(0,nZ*dz,nZ)

x2 = np.linspace(-1*dx,(nX+1)*dx,nX+2)
z2 = np.linspace(-1*dz,(nZ+1)*dz,nZ+2)

# u,rho,dPx,w
def initCondition() :
    k =  1e-4
    m = -1e-3
    init_u = lambda i,j: - 1e1 * np.cos(k * i*dx + m * j*dz)
    init_r = lambda i,j: + 1e-2* np.sin(k * i*dx + m * j*dz)
    init_w = lambda i,j: - 1e-1* np.cos(k * i*dx + m * j*dz)
    init_P = lambda i,j: + 1e2 * np.cos(k * i*dx + m * j*dz)
    u,r,P,w = np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2]), np.zeros([nX+2, nZ+2])
    for i in range(nX+2):
        for j in range(nZ+2):
            u[i][j]   = init_u(i,j)
            r[i][j]   = init_r(i,j)
            w[i][j]   = init_w(i,j)
            P[i][j] = init_P(i,j)
    return (u,r,P,w)

def bound(field):
    (u,r,P,w) = field

    for j in range(nZ+2):
        # u[0][j]=u[-2][j]
        # u[-1][j]=u[1][j]
        # w[0][j]=w[-2][j]
        # w[-1][j]=w[1][j]
        # P[0][j]=P[-2][j]
        # P[-1][j]=P[1][j]
        # r[0][j]=r[-2][j]
        # r[-1][j]=r[1][j]
        u[0][j]=u[1][j]
        u[-1][j]=u[-2][j]
        w[0][j]=w[1][j]
        w[-1][j]=w[-2][j]
        P[0][j]=P[1][j]
        P[-1][j]=P[-2][j]
        r[0][j]=r[1][j]
        r[-1][j]=r[-2][j]

    for i in range(nX+2):
        u[i][ 0]= 0
        u[i][-1]= 0 #u[i][-2]
        w[i][ 0]= 0
        w[i][-1]= 0 #w[i][-2]
        # P[i][ 0]= P[i][-2]
        # P[i][-1]= P[i][1]
        P[i][ 1]= 0#P[i][ 1]
        P[i][-2]= 0#P[i][-2]

        r[i][ 0]= 0 #r[i][ 1]
        r[i][-1]= 0 #r[i][-2]
    return (u,r,P,w)


def step(field) :
    (u,r,P,w) = field

    dPx = lambda i,j: min((P[i+1][j] - P[i][j-1])/(2*dx),(P[i+1][j] - P[i][j])/dx,(P[i][j] - P[i][j-1])/dx)

    update_u = lambda i,j : u[i][j] +  dPx(i,j) /rho0        * dt
    update_r = lambda i,j : r[i][j] -  rho0*Nb**2/g * w[i][j]      * dt

    upper_p = lambda i,j : P[i][j-1] - g * r[i][j-1] * dz
    upper_w = lambda i,j : w[i][j-1] - (u[i+1][j-1]-u[i][j-1])/dx * dz

    lower_p = lambda i,j : P[i][j+1] + g * r[i][j] * dz
    lower_w = lambda i,j : w[i][j+1] + (u[i][j]-u[i-1][j])/dx * dz

    next_u,next_r = np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2])
    next_p,next_w = np.zeros([nX+2, nZ+2]) , np.zeros([nX+2, nZ+2])

    for i in range(1,nX+1):
        for j in range(1,nZ+1):
            next_u[i][j] = update_u(i,j)
            next_r[i][j] = update_r(i,j)

    for j in range(1,nZ+1):
        for i in range(1,nX+1):
            next_p[i][j] = (upper_p(i,j)+lower_p(i,j))/2
            next_w[i][j] = (upper_w(i,j)+lower_w(i,j))/2

    return (next_u,next_r,next_p,next_w)

nowtime = datetime.now().strftime('%m%d_%H%M%S')
number_s = 0
number_v = 0
os.mkdir('./'+nowtime+'s')
os.mkdir('./'+nowtime+'v')
field = initCondition()
U0, Rho0, P0, W0= field

loop = 100
for i in range(loop):
    U, Rho, P, W= field
    if 2*i%loop == 0 :
        X, Z = np.meshgrid(x2,z2)
        M = np.array([[np.sqrt(U[i][j]**2+W[i][j]**2) for j in range(nZ+2)] for i in range(nX+2)])

        plt.quiver( X, Z, U, W, M, units='x') #, pivot='mid',scale=0.05)
        plt.savefig('./'+nowtime+'v/'+"%03.f"%(number_v))
        # plt.clf()
        number_v +=1

    if 2*i%loop == 0 :
        fig = plt.figure()
        ax = fig.add_subplot(111)
        im = ax.imshow(P.T, interpolation='none')
        fig.colorbar(im)
        plt.savefig('./'+nowtime+'s/'+"%03.f"%(number_s))
        number_s += 1
        plt.clf()

    new_field = bound(step(field))
    field = new_field

# fig = plt.figure()
# ax = fig.add_subplot(111)
# im = ax.imshow(P.T, interpolation='none')
# fig.colorbar(im)

# plt.quiver( X, Z, U, W, M, units='x') #, pivot='mid',scale=0.05)
# plt.show()

# print(U-U0)
# print(Rho-Rho0)
# plt.show()
