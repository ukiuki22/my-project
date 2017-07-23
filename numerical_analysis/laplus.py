#緩和法で

from pylab import *

N = 100

def solveLaplus(num,init,bound): 

  def step(field,bound):
    newField = zeros([N+2,N+2])
    for i in range(N+2):
      for j in range(N+2):
        if   (bound[i][j] < 10e10) : newField[i][j] = bound[i][j]
        else :newField[i][j] = (field[i-1][j]+field[i+1][j]+field[i][j-1]+field[i][j+1])/4
    return newField 

  def delta(field,newField):
    d = zeros([N+2,N+2])
    for i in range(N+2):
      for j in range(N+2):
        d[i,j] = abs(newField[i,j] - field[i,j])
    return d.max()
  
  f0 = init
  for n in range(num):
    f1 = step(f0,bound)
    if (n%50 == 0):
      print(n,delta(f1,f0))
    f0 = f1
  return f1

#点電荷
def bound0():
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if ((i==0)or(i==N+1)or(j==0)or(j==N+1)): field[i][j]=0
      elif((i==50)and(j==50)):  field[i][j]=10
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#一様な電場（コンデンサーの中）
def bound1():
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if   (i==  0): field[i][j]= 0
      elif (i==N+1): field[i][j]= N+1
      elif ((j==0)or(j==N+1)):  field[i][j]=i
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#コンデンサー
def bound2():
  field = zeros([N+2,N+2])
  cap1 = lambda i,j : (i==40)and(j>20)and(j<80)
  cap2 = lambda i,j : (i==60)and(j>20)and(j<80)

  for i in range(N+2):
    for j in range(N+2):
      if ((i==0)or(i==N+1)or(j==0)or(j==N+1)): field[i][j]=0
      elif (cap1(i,j)==True): field[i][j]=  -20
      elif (cap2(i,j)==True): field[i][j]=  +20
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#棒磁石
def bound3():
  field = zeros([N+2,N+2])
  Npole = lambda i,j : (i>20)and(i<50)and(j>45)and(j<55)
  Spole = lambda i,j : (i<80)and(i>50)and(j>45)and(j<55)

  for i in range(N+2):
    for j in range(N+2):
      if ((i==0)or(i==N+1)or(j==0)or(j==N+1)): field[i][j]=0
      elif (Npole(i,j)==True): field[i][j]=  +20
      elif (Spole(i,j)==True): field[i][j]=  -20
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#現実的な?棒磁石
def bound4():
  field = zeros([N+2,N+2])
  Npole = lambda i,j : (i>20)and(i<40)and(j>45)and(j<55)
  Spole = lambda i,j : (i<80)and(i>60)and(j>45)and(j<55)
  median= lambda i,j : (i<40)and(i>60)and(j>45)and(j<55)

  for i in range(N+2):
    for j in range(N+2):
      if ((i==0)or(i==N+1)or(j==0)or(j==N+1)): field[i][j]=0
      elif (Npole(i,j)==True): field[i][j]=  +20
      elif (median(i,j)==True):field[i][j]=  +20-2*(i-40)
      elif (Spole(i,j)==True): field[i][j]=  -20
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#針金しゃぼんだま
def bound5():
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if   (i==  0): field[i][j]= j
      elif (i==N+1): field[i][j]= N+1-j
      elif (j==  0): field[i][j]= i
      elif (j==N+1): field[i][j]= N+1-i
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#電場中の導体球
def bound6():
  field = zeros([N+2,N+2])
  sphere = lambda i,j : (i-50)**2+(j-50)**2<20**2

  for i in range(N+2):
    for j in range(N+2):
      if (sphere(i,j)==True): field[i][j] = 0
      elif   (i==  0): field[i][j] = -50
      elif (i==N+1): field[i][j]= N+1-50
      elif ((j==0)or(j==N+1)):  field[i][j]=i-50
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#大きな鞍点が見える解
def bound7():
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if   (i==  0): field[i][j]=  10
      elif (i==N+1): field[i][j]=  10
      elif (j==  0): field[i][j]= -10
      elif (j==N+1): field[i][j]= -10
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#流体の電気伝導度測定
def bound8():
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if ((i==0)or(i==N+1)or(j==0)or(j==N+1)): field[i][j]=0
      elif((i==30)and(j==30)):  field[i][j]= 10
      elif((i==60)and(j==60)):  field[i][j]=-10
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#ななめコンデンサー
def bound9():
  field = zeros([N+2,N+2])
  cap1 = lambda i,j : (i==90)and(j>20)and(j<80)
  cap2 = lambda i,j : (i+j==80)and(j>20)and(j<80)

  for i in range(N+2):
    for j in range(N+2):
      if ((i==0)or(i==N+1)or(j==0)or(j==N+1)): field[i][j]=0
      elif (cap1(i,j)==True): field[i][j]=  -20
      elif (cap2(i,j)==True): field[i][j]=  +20
      #境界でない部分
      else : field[i][j] = 10e10
  return field  

#東工大H26-7
def bound10():
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if   (i==  0): field[i][j]= 0
      elif (i==N+1): field[i][j]= 0
      elif (j==  0): field[i][j]= 0
      elif (j==N+1): field[i][j]= sin(2*3.14/100*i)
      #境界でない部分
      else : field[i][j] = 10e10
  return field  


def grad(field,swich):
  U = zeros([N,N])
  V = zeros([N,N])
  M = zeros([N,N])
  for i in range(1,N+1):
    for j in range(1,N+1):
      x = i-1
      y = j-1
      V[x][y]= -(field[i+1][j]-field[i][j]) #-(field[i+1][j]+field[i-1][j]-2*field[i][j])/2
      U[x][y]= -(field[i][j+1]-field[i][j])#-(field[i][j+1]+field[i][j-1]-2*field[i][j])/2
      M[x][y]= sqrt(V[x][y]**2+U[x][y]**2)
  x_ = arange(N)
  y_ = arange(N)
  X,Y = meshgrid(x_,y_)
  if (swich==0):
  #ベクトル場
    figure()
    Q = quiver( X, Y, U, V, M, units='x', pivot='mid',scale=1)
    axis([30, 50, 30, 50])
    savefig("p1.png")  
    clf()
    quiver( X, Y, U, V, M,pivot='mid') #,scale=1)
    savefig("p2.png")  
    return 
  if (swich==1):
  #流線
    figure()
    streamplot(X, Y, U, V,color='k')
    savefig("p3.png")  
    return 

def init(bound):
  field = zeros([N+2,N+2])
  for i in range(N+2):
    for j in range(N+2):
      if   (bound[i][j] < 10e10) : field[i][j] = bound[i][j]
#緩和しやすいように設定する
      else : field[i][j] = 0*50 + 0*( i -50 )
  return field  


if __name__ == '__main__':
  bound = bound10()
  init  = init(bound)
  grad(init,0)
  clf() 
  imshow(init,extent=[0,1,0,1])
  savefig("q.png")
  clf()
  #print(vec)
  f = solveLaplus(500,init,bound)
  grad(f,0)
  grad(f,1)
  #imshow(f,extent=[100,0,100,0])
  savefig("q.png")