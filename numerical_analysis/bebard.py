#THREE-DIMENTION
# n is 1 only
from pylab import *
#from sympy import *
import matplotlib.pyplot as plt

#Numbers
Ra =  600
Pr =    1
#width
dx = 0.01
dk = 0.1
#mesh
z_range = arange( 0, 1,dx)
x_range = arange(-1, 1,dx)
k_range = arange( 1, 4,dk)
t_range = linspace(0,5,10)

#波数空間での時間発展を記述したのちFurrier変換して元に戻す

def hyp(n):
  x = x_range
  y = x_range
  kc= 3
  phi=n*pi/6
  w = lambda x,y :exp(1j*pi*kc*(sin(phi)*x+cos(phi)*y))
  return array([[w(x,y).real for x in x_range] for y in x_range])

if __name__ == '__main__':
  imshow(hyp(2)+hyp(4))
  show()
"""
#A(kx) complex number
def initWave(kx,,ky,p,q):
  a   = exp( -1*(kx-p)**2 ) #1/shapeness*(kx - peak wn)**2 
  phi = pi*kx#**2
  return a * exp(1j*phi)

#成長率(二次方程式の解の大きいほう)
def sigma(kx):
  s = []
  for i in range(len(kx)):
    kh2 = kx[i]*kx[i]
    n2  = pi*pi+kh2
    b= (1+1/Pr)*n2
    c= 1/Pr*(n2*n2-Ra*(kh2/n2))
    s.append( sqrt(b*b-c)-b ) #xについて解く
  return array(s)

#各時間のwaveのarrayを返す
def stepWave(kx,t):
  a0 = initWave(kx)
  a1 = a0
  a = [a0]
  s = sigma(kx)
  for i in range(len(t)):
    a1 = a0*exp(s*t[i])
    a.append(a1)
  return a

def realwave2dim(A):
  kx = k_range
  W0 = lambda x,z: sum([A[i]*exp(1j*kx[i]*x)*dk*sin(pi*z) for i in range(len(kx)) ] ).real
  return array([[abs(W0(x,z)) for x in x_range] for z in z_range])

def realwave1dim(A):
  kx = k_range
  W0 = lambda x: sum([A[i]*exp(1j*kx[i]*x)*dk for i in range(len(kx)) ] ).real
  return array([W0(x) for x in x_range])

#TODO:各時間ごと=stepWave(k_range,t_range)[i]の実空間表示（フーリエ変換）＜＝一つの関数作れば（フーリエ変換）あとはそれを何度も使う
#     2変数に拡張できるように考える 成長率を正しい標識に

if __name__ == '__main__':
#  imshow(realwave(initWave(k_range)))
  for i in range(len(t_range)):
    #plot(k_range, abs(stepWave(k_range,t_range)[i]) )
    #plot(x_range, realwave1dim(stepWave(k_range,t_range)[i]))
    imshow(realwave2dim(stepWave(k_range,t_range)[i]))
    savefig(str(i)+".png")
    clf()
  #show()

  print(sigma(k_range))

    kh2 = kx[i]*kx[i]
    n2  = pi*pi+kh2
    eq = Eq( (x+n2)*(x+n2/Pr)-Ra/Pr*(kh2/n2),0) 
    s.append( (kx[i],solve(eq,x) )) #xについて解く
  
#  print ( stepWave(k_range,t_range) )
  for i in range(len(t_range)):
    plot (k_range, abs(stepWave(k_range,t_range)[i]) )
    #savefig(str(i)+".png")
    #clf()
  show()


#initialcondition from wave-space to x-space
def init(A):
  kx = k_range
  W0 = lambda x: sum([A[i]*exp(1j*kx[i]*x)*dk*sin(pi*0.5) for i in range(len(kx)) ] ).real
  fig = plt.figure()
  xlabel("x")
  ylabel("W")
  plt.plot(x_range,array(list(map(W0,x_range))))
  return array(list(map(W0,x_range)))

def image2D(A):
  kx = k_range
  def w(X,Z):
    W0 = lambda x,z: sum([A[i]*exp(1j*kx[i]*x)*dk*sin(pi*z) for i in range(len(kx)) ] ).real
    return [[W0(x,z) for x in X] for z in Z]
#  fig = plt.figure()
#  bar=plt.imshow(array(w(x_range,z_range)),extent=[-1,1,0,1])
#  plt.title("init")
#  plt.xlabel('X')
#  plt.ylabel('Z')
#  plt.colorbar(bar)
  return array(w(x_range,z_range))

def initWaveNumberSpace(A):
#  fig = plt.figure()
#  xlabel("kx")
#  ylabel("A")
#  plt.plot(k_range,abs(A))
  return abs(A)

if __name__ == '__main__':
  fig = plt.figure()
  ax = fig.add_subplot(211)
  bar=plt.imshow(image2D(A(k_range)),extent=[-1,1,0,1])
  plt.title("init")
  plt.xlabel('X')
  plt.ylabel('Z')
  plt.colorbar(bar)
  ax = fig.add_subplot(212)
  plt.plot(k_range,initWaveNumberSpace(A(k_range)))
  plt.show()
  #init(A(k_range))
  #initWaveNumberSpace(A(k_range))

#w(kx) use sympy

#composit as W(x,z,t)


"""
