import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

g = 9.8     # 重力定数
m = 1.0     # 質量
h = 10      # 初期位置
# G 1e-11 質量1e10~30 /　距離1e6~10 ^2  
G = 1e-11

# 計算するインターバル
t = np.arange(0, 1, 0.01) #5くらいがよい

"""
#ピタゴラス
M1 = 3*1e11
M2 = 4*1e11
M3 = 5*1e11
[3/5.,0]#
[0,4/5.]#
[0,0]#
theta_1=0
theta_2=-60
theta_3=240
theta_4=0
theta_5= 90
theta_6= 90

r1=0
r2=1
r3=1
r4=0
r5=0
r6=0
"""

#カオス
M1 = 3*10e11
M2 = 4*10e11
M3 = 5*10e11

theta_1=0
theta_2=80
theta_3=200
theta_4=0
theta_5=0
theta_6=0

r1=0
r2=1.
r3=1.
r4=0
r5=0
r6=0
"""

#ほぼ３角形
M1 = 10e11
M2 = 10e11
M3 = 10e11

theta_1=0.1
theta_2=120
theta_3=240
theta_4=90
theta_5=210
theta_6=330

r1=1.
r2=1.
r3=1.
r4=1.
r5=1.
r6=1.
"""


def threebody2D(xs,t):
  x1 = xs[0]
  y1 = xs[1]
  x2 = xs[2]
  y2 = xs[3]
  x3 = xs[4]
  y3 = xs[5]

  r12  = np.sqrt( (x1-x2)**2+(y1-y2)**2 )
  r23  = np.sqrt( (x2-x3)**2+(y2-y3)**2 )
  r31  = np.sqrt( (x3-x1)**2+(y3-y1)**2 )

  g12x= - (G*M2/ r12**3) * (x1 - x2)
  g12y= - (G*M2/ r12**3) * (y1 - y2)
  g13x= - (G*M3/ r31**3) * (x1 - x3)
  g13y= - (G*M3/ r31**3) * (y1 - y3)

  g23x= - (G*M3/ r23**3) * (x2 - x3)
  g23y= - (G*M3/ r23**3) * (y2 - y3)
  g21x= - (G*M1/ r12**3) * (x2 - x1)
  g21y= - (G*M1/ r12**3) * (y2 - y1)

  g31x= - (G*M1/ r31**3) * (x3 - x1)
  g31y= - (G*M1/ r31**3) * (y3 - y1)
  g32x= - (G*M2/ r23**3) * (x3 - x2)
  g32y= - (G*M2/ r23**3) * (y3 - y2)


  mat = np.zeros((2*3*2,2*3*2))
  mat[0,6] +=1.
  mat[1,7] +=1.
  mat[2,8] +=1.
  mat[3,9] +=1.
  mat[4,10] +=1.
  mat[5,11] +=1.

  #xs  = [1,2,3,4,5,6,7,8,9,1,2,3]
  cst = np.array([0,0,0,0,0,0, \
                  g12x+g13x,g12y+g13y,\
                  g23x+g21x,g23y+g21y,\
                  g31x+g32x,g31y+g32y \
                  ])
  return mat.dot(xs)+cst

def f(xv,t):
  return threebody2D(xv,t)

def r(r,deg):
  rad =( np.pi/180. )* deg
  x = np.cos(rad)
  y = np.sin(rad)
  return [r*x,r*y]

def i32():
  x1 = r(r1,theta_1)
  x2 = r(r2,theta_2)
  x3 = r(r3,theta_3)
  u1 = r(r4,theta_4)
  u2 = r(r5,theta_5)
  u3 = r(r6,theta_6)
  xv = np.array(x1+x2+x3+u1+u2+u3)
  I  = odeint(f, xv, t)
  x1 = I.T[0]
  y1 = I.T[1]
  x2 = I.T[2]
  y2 = I.T[3]
  x3 = I.T[4]
  y3 = I.T[5]
  #xG = (M1*x1+M2*x2)/(x1+x2)
  #yG = (M1*y1+M2*y2)/(y1+y2)
  """
  for i in range(len(x1)):
    plt.plot(x1[i],y1[i],"ro")
    plt.plot(x2[i],y2[i],"bo")
    plt.plot(x3[i],y3[i],"yo")
    title = str(theta_1)+","+str(theta_2)+","+str(theta_3)+" "
    plt.title(r"$\theta =$" +title)
    plt.xlim(-1.2,1.2)
    plt.ylim(-1.2,1.2)
    plt.savefig('nb2/'+title+'num'+str(i)+'.png')
    plt.clf()
    print(i)
  return
    """
  plt.plot(x1,y1,"r-")
  plt.plot(x2,y2,"b-")
  plt.plot(x3,y3,"y-")
  plt.title(str(theta_1)+", "+str(theta_2)+", "+str(theta_3)+" ")
 # plt.ylim(-1,1)
 # plt.xlim(-4/3.,4/3.)
  plt.show()
  return

def i32save():
  x1 = r(r1,theta_1)
  x2 = r(r2,theta_2)
  x3 = r(r3,theta_3)
  u1 = r(r4,theta_4)
  u2 = r(r5,theta_5)
  u3 = r(r6,theta_6)
  xv = np.array(x1+x2+x3+u1+u2+u3)
  I  = odeint(f, xv, t)
  x1 = I.T[0]
  y1 = I.T[1]
  x2 = I.T[2]
  y2 = I.T[3]
  x3 = I.T[4]
  y3 = I.T[5]
  
  for i in range(len(x1)):
    plt.axes(axisbg="#000000") # 背景を灰色に.
    plt.plot(x1[i],y1[i],"ro")
    plt.plot(x2[i],y2[i],"bo")
    plt.plot(x3[i],y3[i],"yo")
    title = str(theta_1)+","+str(theta_2)+","+str(theta_3)+" "
    plt.title(r"$\theta =$" +title)
    plt.xlim(-1.2,1.2)
    plt.ylim(-1.2,1.2)
    plt.savefig('nb2/'+title+'num'+str(i)+'.png')
    plt.clf()
    print(i)
  return

def main(): 
  return i32()

if __name__ == '__main__':
  main()

"""
def twebody2D(xs,t):
  x1 = xs[0]
  y1 = xs[1]
  x2 = xs[2]
  y2 = xs[3]
  r  = np.sqrt( (x1-x2)**2+(y1-y2)**2 )
  g1x= - (G*M2/ r**3) * (x1 - x2)
  g1y= - (G*M2/ r**3) * (y1 - y2)
  g2x= + (G*M1/ r**3) * (x1 - x2)
  g2y= + (G*M1/ r**3) * (y1 - y2)

  mat = np.zeros((8,8))
  mat[0,4] +=1.
  mat[1,5] +=1.
  mat[2,6] +=1.
  mat[3,7] +=1.

  xs  = np.array(xs)
  cst = np.array([0,0,0,0,g1x,g1y,g2x,g2y])
  return mat.dot(xs)+cst


def i22():
  x1 = [0 ,0]
  x2 = [1e1 ,0]
  u1 = [0 ,0]
  u2 = [0 ,1e1]
  xv = np.array(x1+x2+u1+u2)
  I  = odeint(f, xv, t)
  x1 = I.T[0]
  y1 = I.T[1]
  x2 = I.T[2]
  y2 = I.T[3]
  #xG = (M1*x1+M2*x2)/(x1+x2)
  #yG = (M1*y1+M2*y2)/(y1+y2)
  plt.plot(x1,y1,"ro")
  plt.plot(x2,y2,"bo")
  #plt.plot(xG,yG,"yo")
  plt.show()
  return

def main(): 
  return i22()


#----------------#
def onebody2D(xs,t):
  x1 = xs[0]
  y1 = xs[1]
  r1 = np.sqrt(x1**2 + y1**2)
  g1x = -(GM/ r1**3) * x1
  g1y = -(GM/ r1**3) * y1

  mat = np.zeros((4,4))
  mat[0,2] +=1.
  mat[1,3] +=1.

  xs  = np.array(xs)
  cst = np.array([0,0,g1x,g1y])
  return mat.dot(xs)+cst


def i12():
  xv = [1,0,0,0.1]
  I = odeint(f, xv, t)
  x1 = I.T[0]
  y1 = I.T[1]
  plt.scatter(x1,t)
  plt.scatter(y1,t)
  plt.show()
  return


def twebody1Dpre(xs,t):
  mat = np.array([ [0,1],[0,0] ])
  xs  = np.array(xs)
  cst = np.array([0,-GM/(xs[0]**2)])
  ret = mat.dot(xs)+cst
  return ret

def onebody1D(xs,t):
  mat1 = np.array([ [0,1],[0,0]])
  xs   = np.array(xs)#[ x[0], x[1] ])
  cst  = np.array([ 0   , -g/m ])

  ret  = mat1.dot(xs)+cst
  return ret



def i11():
      # 初期状態
    xv = [h,0]
    # 積分する
    I = odeint(f, xv, t)
    x = I.T[0]
    plt.scatter(t,x)
    plt.show()
    return 

"""


"""
# Array1*N -> Array1*N ->
def threebody(x, t):
    f = [0]*len(x)
    Ms = 330000
    Me = 1
    Mm = 0.1
    D1 = ((x[4]-x[0])**2+(x[6]-x[2])**2)**(3/2)
    D2 = (x[0]**2+x[2]**2)**(3/2)
    f[0] = x[1]
    f[1] = 4*np.pi**2*(Me/Ms*(x[4]-x[0])/D1-x[0]/D2)
    f[2] = x[3]
    f[3] = 4*np.pi**2*(Me/Ms*(x[6]-x[2])/D1-x[2]/D2)
    D2 = (x[4]**2+x[6]**2)**(3/2)    
    f[4] = x[5]
    f[5] = 4*np.pi**2*(Mm/Ms*(x[0]-x[4])/D1-x[4]/D2)
    f[6] = x[7]
    f[7] = 4*np.pi**2*(Mm/Ms*(x[2]-x[6])/D1-x[6]/D2)
    return f

v0 = [1.52, 0, 0, -4.6, 1, 0, 0, -5.1]
t = np.arange(0, 5, 0.01)

v = odeint(threebody, v0, t)

#------
def onebody(x0,t):
  arr = [[0,1],[0,0]]
  cst = [[0],[-1]]
  a = np.array(arr) 
  c = np.array(cst)
  xs= (np.array(x0))[:, np.newaxis]
  return list(a.dot(xs) + c)

def f(x,t):
  return onebody(x,t)

def main():
  x0 = [1,1]
  t  = np.arange(0,0.5,0.1)
  x  = odeint(f,x0,t)
  print(x)#f(x0,t))

"""