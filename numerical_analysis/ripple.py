# -＊- coding: UTF-8 -＊-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#風紋シミュレータ  
N=100 		#NxN Field
L=3.0		#風速
h=0.1		#単位砂
k=1.		#流され係数
D=1/10.		#拡散係数



# Size -> Field
def init():
	mount    = 1.00
	f        = np.zeros((N,N))
	for i in range(N):
		for j in range(N):
	#	f[50,i]   = mount
			f[j,i] += np.random.rand()*(3.15-2.84)+2.84
	return f

# Field -> Field
def updateField(f):
	for i in range(N):
		for j in range(N):
			f = diffuse(f,i,j)
			f = flow(f)
	return f

def up(n):
	f = init()
	for i in range(n): 
		updateField(f)
		if (i%15==0):
			image(f,i)
			surface3D(f,i)
			print(i)
	return


def image(f,i):
	plt.imshow(f)
	plt.savefig(str(i)+'.png')
	plt.clf()
	return

def wire3D(f,i):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	x = np.arange(0, N, 1.0)
	y = np.arange(0, N, 1.0)
	X, Y = np.meshgrid(x, y)
	Z = f
	ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
	ax.set_zlim(0, 70)
	plt.savefig('d'+str(i)+'.png')
	plt.clf()
	return 0

def surface3D(f,i):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	x = np.arange(0, N, 1.0)
	y = np.arange(0, N, 1.0)
	X, Y = np.meshgrid(x, y)
	Z = f
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
	ax.set_zlim(0, 10*3)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
	#fig.colorbar(surf, shrink=0.5, aspect=5)
	plt.savefig('s'+str(i)+'.png')
	plt.clf()
	return 

def line(f,i,y0):
	plt.xlim(0,100)
	plt.ylim(0,5.0)
	lin=f[y0]
	plt.plot(lin)
	plt.savefig('p'+str(i)+'.png')
	plt.clf()
	return

# PositionX -> PositonX
def p(x):
	x = x%N
	return x

#Field -> Field
def diffuse(f,i,j):
	f[i,j]= (1-D)  * f[i  ,j  ]  \
		   +(D/6.) *(f[p(i+1),  j   ]+f[   i-1,j  ]+f[i  ,p(j+1)]+f[i  ,j-1]) \
		   +(D/12.)*(f[p(i+1),p(j+1)]+f[p(i+1),j-1]+f[i-1,p(j+1)]+f[i-1,j-1])
	return f

#Field -> Field
def flow(f):
	x0 = np.random.randint(N)
	y0 = np.random.randint(N)
	x =   x0 
	y = p(y0 + int(L * k * f[x0,y0]) )
	#if (f[x0,y0]> h):
	f[x0,y0]-=h
	f[x ,y ]+=h
	return f

if __name__ == '__main__':
	up(int(input("n")))