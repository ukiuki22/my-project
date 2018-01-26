# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('ggplot')
fig = plt.figure()
ims = []

"""
風上差分で1次元非斉次非粘性Burgers方程式を解く
--うまくいかない（緩和しない，もとからな気がして来た）
--1次元計算じゃ圧力勾配あったら逃げ場がないから発散する？
"""

dx,nX =  100 ,1000 #m
dt,nT =   10 ,10 #sec
c = 0 #100 #m/s

x = np.linspace(0,nX*dx,nX)
x2 = np.linspace(0,nX*dx,nX+2)
# t = np.linspace(0,nT*dt,nT)

# initCondition = [1 for i in range(int(0.25*nX))] + [0 for i in range(int(0.75*nX))]
# initCondition = [c + 1 * np.sin(2*np.pi*x/(0.5*nX*dx))[i] for i in range(int(0.5*nX))] + [c for i in range(int(0.5*nX))]
initCondition = [c for i in range(nX)]

# pressGrad = -0.01 * np.cos(2*np.pi*x2/(nX*dx))

pressGrad = 1/50*(x/(nX*dx)-0.5) * np.exp(-50*(x/(nX*dx)-0.5)**2)
# plt.plot(pressGrad)

def step(u) :
    f = lambda u,j: 0.5 * u[j] * u[j]

    def f_foward(u,j):
        if(u[j+1]+u[j] >0) : return u[j]*u[j]/2
        else : return u[j+1]*u[j+1]/2

    def f_back(u,j):
        if(u[j+1]+u[j] >0) : return u[j-1]*u[j-1]/2
        else : return u[j]*u[j]/2

    func = lambda u,j : u[j] -  (dt/dx) * (f_foward(u,j) - f_back(u,j)) + dt * pressGrad[j]

    #境界ダミー以外の部分を計算．実データの範囲は[1,nX-1]（端っこもダミーデータのおかげで計算可能）
    next_u = [0] + [ func(u,j) for j in range(1,nX-1)] + [0]
    #境界条件
    next_u[ 0  ] = c #next_u[nX-2]
    next_u[nX-1] = c #next_u[   1]
    return next_u

#境界のために両端に加える
u = [c] + initCondition + [c]

momentum,energy = [],[]
for i in range(nT):
    # momentum += [sum(u)/len(u)]
    # energy += [sum([u[i]**u[i] for i in range(len(u))])/len(u)]
        # if (i%500==0):
        #     im = plt.plot(u,label=str(i*dt)+' sec')
            # ims.append(im)

    if (i%int(nT/10)==0):
        im = plt.plot([i*dx/1e3 for i in range(len(u))] ,u,'black',label=str(i*dt)+' sec')
        ims.append(im)
    u_next = step(u)
    u      = u_next


# print(u)
# plt.plot(energy)
# plt.plot(momentum)
# plt.legend()
ani = animation.ArtistAnimation(fig, ims, interval=500)
plt.show()
# ani.save("burgers2.gif", writer="imagemagick")
