# -＊- coding: UTF-8 -＊-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

plt.style.use('ggplot')
mount = pd.read_csv("export_bipolar.vtk",header=None)


def readNode(filePath):
  data  = pd.read_csv(filePath,header=None)
  return [float(data.ix[0,0].lstrip('['))]+[data.ix[0,i] for i in range(1, data.shape[0]*data.shape[1]-1)]+[float(data.ix[0,data.shape[0]*data.shape[1]-1].rstrip(']'))]

def importScalar(filePath):
  data  = pd.read_csv(filePath,header=None)
  return [data.ix[0,i] for i in range(1, data.shape[0]*data.shape[1]-1)]

#--------Stress( Tensor )-----------#

#tensor2list_2 :: Int -> Int -> Int -> Tensor U -> [Double]
#tensor2list_2 a b numt t = [t!(Z:.i:.j:.a:.y:.b)| i<-[0..2], j<-[0..2], y<-[0..numt-1]]

def importTensor(filePath):
 # 3,3,(q+2),(r+2)の４次元配列を3*3,(q+2)*(r+2)2次元配列として収納
  row  = pd.read_csv(filePath,header=None)
  #[]の処理
  #(l,r)=(float(row[0][0][1:]),float(row[len(row.columns)-1][0][:-1]))
  data = [row[i][0] for i in range(1,len(row.columns)-1)] #[l] + [row[i][0] for i in range(1,len(row.columns)-1)] + [r]
  return list(zip(*[iter(data)]*9))

def misesStress(filePath):
  s = importTensor(filePath)
  mises = lambda s11,s12,s13 ,s21,s22,s23 ,s31,s32,s33 : np.sqrt(1/2*((s11-s22)**2+(s22-s33)**2+(s33-s11)**2+3*(s12**2+s21**2+s13**2+s31**2+s23**2+s32**2)))
  return [mises(s[i][0],s[i][1],s[i][2],s[i][3],s[i][4],s[i][5],s[i][6],s[i][7],s[i][8]) for i in range(len(s))]

#------------------------------#


def makevtk(p,q,r,num1,num2,j,currentDrectry,commands):

  #Node情報が入っている行数
  rNode = lambda p,q,r: range(mount[mount[0].str.contains("CELLS")].index[0]-5) #CELLS 4000 84000の前の行-5
  #Scalar値が入っている行数
  rScalar = range(len(mount)-mount[mount[0].str.contains("LOOKUP_TABLE")].index[0]-1) # LOOKUP_TABLE defaultの次の行から最後の行まで
  #Scalar値が始まる行数
  beginScalar = mount[mount[0].str.contains("LOOKUP_TABLE")].index[0]+1 # LOOKUP_TABLE defaultの次の行

  if(commands[0]==1):
    nodelist = lambda i : readNode(currentDrectry+"/data_"+str(num1)+"/outputNode_"+str(i)+"/"+str(num1-num2*j)+".txt")
    node = [nodelist(i) for i in range(3)] #xyz
    #5-3304にnodeデータ
    for i in rNode(p,q,r):  mount.ix[5+i] = str(node[0][0+i]) + " " + str(node[1][0+i]) + " " +str(node[2][0+i])

  if(commands[0]==2): #強調
    nodelist = lambda i : np.array(readNode(currentDrectry+"/data_"+str(num1)+"/outputNode_"+str(i)+"/"+str(num1-num2*j)+".txt"))
    baselist = lambda i : np.array(readNode(currentDrectry+"/data_"+str(num1)+"/outputNode_"+str(i)+"/"+str(num1       )+".txt"))
    overstate = lambda i : list(nodelist(i)+10e4*(nodelist(i)-baselist(i)))
    node0 = overstate(0)
    node1 = overstate(1)
    node2 = overstate(2)
    for i in rNode(p,q,r):  mount.ix[5+i] = str(node0[0+i]) + " " + str(node1[0+i]) + " " +str(node2[0+i])

  if(commands[1]==0): #test
    orz = [i for i in rScalar]
    for i in rScalar :  mount.ix[beginScalar+i]=str(orz[0+i])

  if(commands[1]==1):
    press = lambda r_ :importScalar(currentDrectry+"/data_"+str(num1)+'/outputpressure_f'+str(r_)+'/'+str(num1-num2*j)+'.txt')
    presslist = reduce ( (lambda x,y:x+y), [ press(i) for i in range(1,r+1)] )
    #print(len(presslist))
    presslistAdd0 = presslist+[0 for i in range(3*q*r)]
    for i in rScalar :  mount.ix[beginScalar+i]=str(presslistAdd0[0+i])

  if(commands[1]==2): #全部にpressデータ
    namelist = [i for i in range(num1+1) if i%num2==0]
    press = lambda r_ :importScalar(currentDrectry+"/data_"+str(num1)+'/outputpressure_f'+str(r_)+'/'+str(namelist[-j-1])+'.txt')
    presslist = reduce ( (lambda x,y:x+y), [ press(i) for i in range(1,r+1)] )
    #print(len(presslist))
    presslistAdd0 = presslist*4 #+[0 for i in range(3*q*r)]
    for i in rScalar :  mount.ix[beginScalar+i]=str(presslistAdd0[0+i])

  if(commands[1]==3):
  #特定のzのpressデータをマスクしたいとき、z<=2,z>=numz-1
  #絶対値
    namelist = [i for i in range(num1+1) if i%num2==0]
    def press(r_):
      if(r_ in [1,2,r-1,r]) :
        return [0 for i in range(q)]
      else :
        return importScalar(currentDrectry+"/data_"+str(num1)+'/outputpressure_f'+str(r_)+'/'+str(namelist[-j-1])+'.txt')

    presslist = reduce ( (lambda x,y:x+y), [ press(i) for i in range(1,r+1)] )    #print(len(presslist))
    presslistAdd0 = list(abs(np.array(presslist*4))) #+[0 for i in range(3*q*r)]
    for i in rScalar :  mount.ix[beginScalar+i]=str(presslistAdd0[0+i])

  mount.to_csv( currentDrectry+"/data_"+str(num1)+'/p'+str(j)+'.vtk', index=False ,header=False)

  if(commands[2]==1): #plot
    for i in range(1,r+1):
      y = press(i)
      plt.plot(y,label=str(i))
  plt.legend()
  plt.savefig(currentDrectry+"/data_"+str(num1)+'/q'+str(j)+'.png')
  plt.clf()
  return


def main(cd):
  #data = pd.read_csv(cd+'/data.txt',header=None)
  #nums = pd.read_csv(cd+'/p_numbers.csv',header=None)

  (p,q,r) = (1,100,10)#(nums[0][0]-1,nums[0][2],nums[0][3])
  (num1,num2) = (50,1)#(data[0][0],data[1][0])

  #(p,q,r) = (1,100,10)
  #(ncum1,num2) = (1000,100)
  #num1 = int ( input("number") )
  print('(p,q,r)='+str((p,q,r)))
  print('(num1,num2) ='+str((num1,num2)))

  for j in range(100):
    makevtk(p,q,r,num1,num2,j,cd,[0,2,1])
    print(j)

if __name__ == '__main__':
  main(".")
  #cds = [201,202,203,204] #[251,252,253,254,401,402,403,404]#[301,302,303,304]#[201,202,203,204,401,402,403,404]
  #for i in range(len(cds)):
  #  main(str(cds[i]))
