import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt
from functools import reduce 

#気体のモデル
N  = 10000
L  = 1.0

dt = 0.05
num = 50 #00
rN = range(N)

#InitialPosition
X0 = list(rand(2*N)*2-1) #[0.5 for i in range(2*N)]#
#InitialVelocity
V0 = list(randn(2*N))

plt.style.use('ggplot') 
fig = plt.figure()



##### MOTION ##### 
update = lambda X,V : list( map(lambda x,v: x+v*dt , X,V))

def wall(X,V): #V = wall(X,V) 壁による反射
  for i in rN:
    V[i] = -V[i] if abs(X[i])>L else V[i] 
  return V


#### ####

#def hall
#def press
#def vHist

def xDistribute(X):
  X1 = [X[2*i  ] for i in rN]
  Y1 = [X[2*i+1] for i in rN]
  p = lambda x : x > 0 
  n = lambda x : x < 0 
  return len( list( filter( p ,X1)))

def press(X):
  p = lambda x : abs(x)> L
  return len( list( filter( p ,X)))


def main(num):
  X = X0
  V = V0

  dis =  [0 for i in range(20)]
  pres = [0 for i in range(20)]

  for i in range(num):
    X1 = update(X,V)
#Outputs
    del  dis[0]
    del pres[0]
    dis  +=[xDistribute(X)]
    pres +=[press(X)]

    plotf(i,X1,[]) #[dis,pres])
#次にデータを渡す
    X  = X1
    V = wall(X1,V)

    #dis.append(xDistribute(X))
    #pres.append(press(X))
  #plt.plot(dis)
  #plt.plot(pres)
  #plt.savefig('dis_press.png')



def plotf(i,X,option):
  x = [X[2*i  ] for i in rN]
  y = [X[2*i+1] for i in rN]  

  ax = fig.add_subplot(111,aspect=1.0)
  ax.scatter(x,y,color='orange',s=1) 
  ax.set_xlim(-L*1.1,L*1.1)
  ax.set_ylim(-L*1.1,L*1.1)

  for j in range(len(option)):
    plt.axes([0.3, 0.2, 0.3, 0.2]) #axes([左, 下, 幅, 高さ])
    plt.plot(option[j])

  if (i<10):  plt.savefig('gasfig/fig0'+str(i)+'.png')
  else :      plt.savefig('gasfig/fig' +str(i)+'.png')
  print(i)
  plt.clf()



if __name__ == '__main__':
  main(num)