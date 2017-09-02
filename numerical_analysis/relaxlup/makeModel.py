# -＊- coding: UTF-8 -＊-
from math import *
import numpy as np

Ro  = 30.03/1000  #外管半径
Ri  = 30.00/1000  #内管半径
eps = 0.95        #偏心率
n   = 100         #ξ方向に切る数
r   = 1           #η方向に切る数--流体
L   = 1.0/100     #管の長さ
l   = 10 #int(input("numz="))           #管をz方向に切る数
r_i = 2           #内管をr方向に切る数
r_o = 1           #外管をr方向に切る数
w_i = 0.3/1000    #内管の1層の厚さ
w_o = 0.3/1000    #外管の1層の厚さ
dig = 0.5e-7      #外管にめり込む量（最大値） * dig < w_o
para = 5.0e-7     #平行移動後の内管と外管の間の最も狭い部分の長さ

a = Ri / Ro #半径比
S = (1 + a)/(2*eps) * sqrt((1 - eps**2) * (1 - ((1 - a)/(1 + a)*eps)**2)) #定数
c = S * Ro #定数

eta_i = log((S/a) + sqrt(1 + (S/a)**2))
eta_o = log(S + sqrt(1 + S**2))

r1 = (eta_i - eta_o)/r #流体の1層の厚み
dl = L/l #z軸方向の層の厚み

#bipolarの2つの中心を求める
center_01=[((c*sinh(eta_i)/(cosh(eta_i) - cos(0.0))) + (c*sinh(eta_i)/(cosh(eta_i) - cos(pi))))/2, (c*sin(0.0)/(cosh(eta_i) - cos(0.0)) + c*sin(pi)/(cosh(eta_i) - cos(pi)))/2, 0.0]
center_02=[((c*sinh(eta_o)/(cosh(eta_o) - cos(0.0))) + (c*sinh(eta_o)/(cosh(eta_o) - cos(pi))))/2, (c*sin(0.0)/(cosh(eta_o) - cos(0.0)) + c*sin(pi)/(cosh(eta_o) - cos(pi)))/2, 0.0]

#2点間の距離を求める
def length(x,y):
  return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)

#3点x-o-yの角度を求める
def phi(x,y,o):
  a = length(x,y)
  b = length(y,o)
  c = length(x,o)
  if ((b**2+c**2-a**2)/(2*b*c)+1>-1.0e-5)and((b**2+c**2-a**2)/(2*b*c)+1<0): return acos(-1)
  elif ((b**2+c**2-a**2)/(2*b*c)-1>0)and((b**2+c**2-a**2)/(2*b*c)-1<1.0e-5): return acos(1)
  else: return acos((b**2+c**2-a**2)/(2*b*c))

#座標番号の管理
def f(i,j,k,r):
  return k+n*j+i*r*n

#vtk形式で座標の保存
def vtk_node(fileobj,nodelist):
  for i in range(len(nodelist)):
    for j in range(3):
      fileobj.write("%f " %nodelist[i][j])
    fileobj.write("\n")
  return

#vtk形式で20点メッシュの保存
def vtk_mesh(fileobj,meshlist):
  for i in range(len(meshlist)):
    fileobj.write("20 ")
    for j in range(1,21):
      fileobj.write("%d " %(meshlist[i][j]-1))
    fileobj.write("\n")
  return

#abaqus形式で座標の保存
def inp_node(fileobj,nodelist,a):
  for i in range(len(nodelist)):
    fileobj.write("%10d,  " %(i+a+1))
    for j in range(3):
      fileobj.write("%-15f,  " %nodelist[i][j])
    fileobj.write("\n")
  return

#abaqus形式で20点メッシュの保存
def inp_mesh(fileobj,meshlist):
  for i in range(len(meshlist)):
    for j in range(21):
      fileobj.write("%10d" %meshlist[i][j])
      if j==20: break
      fileobj.write(",")
    fileobj.write("\n")
  return

#hypermesh形式で座標の保存
def fem_node(fileobj,nodelist,a):
  for i in range(len(nodelist)):
    fileobj.write("GRID")
    fileobj.write("%12d        " %(i+a+1))
    for j in range(3):
      fileobj.write("%s" %(str(round(nodelist[i][j],8)).ljust(8)[0:8]))
    fileobj.write("\n")
  return

#hypermesh形式で20点メッシュの保存
def fem_mesh(fileobj,meshlist):
  for i in range(len(meshlist)):
    fileobj.write("CHEXA   ")
    for j in range(22):
      if j==0: fileobj.write("%8d" %meshlist[i][0])
      elif j==1:  fileobj.write("       0")
      elif j==7:  fileobj.write("%8d \n" %meshlist[i][j-1])
      elif j==8:  fileobj.write("+       %8d" %meshlist[i][j-1])
      elif j==15: fileobj.write("%8d \n" %meshlist[i][j-1])
      elif j==16: fileobj.write("+       %8d" %meshlist[i][j-1])
      else: fileobj.write("%8d" %meshlist[i][j-1])
    fileobj.write("\n")
  return

#hypermeshの20点要素の並び順が他と異なるのでhypermesh用に加工
def change20node(meshlist):
  for i in range(len(meshlist)):
    a = meshlist[i][13:17]
    b = meshlist[i][17:]
    meshlist[i][13:17] = b
    meshlist[i][17:] = a
  return meshlist

#solverで計算ができるようにxyzの境界に配列を付け足す
def addcoord(arrg,p,q,r):
  #addmetricの代わり
  arrg2 = np.zeros((p+2,q+2,r+2))
  arrg2[1:p+1,1:q+1,1:r+1] = arrg[:,:,:]
  #z
  arrg2[:,:,0] = arrg2[:,:,1]
  arrg2[:,:,r+1] = arrg2[:,:,r]
  #y 周期的境界条件
  arrg2[:,0,:] = arrg2[:,q,:]
  arrg2[:,q+1,:] = arrg2[:,1,:]
  #x
  arrg2[0,:,:] = arrg2[1,:,:]
  arrg2[p+1,:,:] = arrg2[p,:,:]
  return arrg2

#yzのみ境界に配列を付け足す
def onlyyz(arrg,p,q,r):
  #addmetricの代わり
  arrg2 = np.zeros((p,q+2,r+2))
  arrg2[0:p,1:q+1,1:r+1] = arrg[:,:,:]
  #z
  arrg2[:,:,0] = arrg2[:,:,1]
  arrg2[:,:,r+1] = arrg2[:,:,r]
  #y
  arrg2[:,0,:] = arrg2[:,q,:]
  arrg2[:,q+1,:] = arrg2[:,1,:]
  return arrg2

def set_twnid(arrg,twn,p,q,r):
  numf = p*q*r
  twnid = arrg.reshape(numf)
  twnid = twnid.astype(int)
  new = np.zeros((numf,20))
  num = 0
  while num<numf:
    new[num,:] = twn[twnid[num]-1,:]
    num += 1

  return new.astype(int)

#流体部分
def fluid_grid():
  #座標
  #8点メッシュの座標
  list_grid_01 = [[c*sinh(eta_o+j*r1)/(cosh(eta_o+j*r1) - cos(2*pi/n*(n-k))), c*sin(2*pi/n*(n-k))/(cosh(eta_o+j*r1) - cos(2*pi/n*(n-k))), i*dl]\
   for i in range(l+1) for j in range(r+1) for k in range(n)]
  #θ方向に隣り合った点の中点
  list_grid_02 = [[c*sinh(eta_o+j*r1)/(cosh(eta_o+j*r1) - cos(2*pi/n*(n-k-0.5))), c*sin(2*pi/n*(n-k-0.5))/(cosh(eta_o+j*r1) - cos(2*pi/n*(n-k-0.5))), i*dl]\
   for i in range(l+1) for j in range(r+1) for k in range(n)]
  #r方向に隣り合った点の中点
  list_grid_03 = [[c*sinh(eta_o+(j+0.5)*r1)/(cosh(eta_o+(j+0.5)*r1) - cos(2*pi/n*(n-k))), c*sin(2*pi/n*(n-k))/(cosh(eta_o+(j+0.5)*r1) - cos(2*pi/n*(n-k))), i*dl]\
   for i in range(l+1) for j in range(r) for k in range(n)]
  #z方向に隣り合った点の中点
  list_grid_04 = [[c*sinh(eta_o+j*r1)/(cosh(eta_o+j*r1) - 1.0), 0.0, (i+0.5)*dl] if k==0 else [c*sinh(eta_o+j*r1)/(cosh(eta_o+j*r1) - cos(2*pi/n*(n-k))), c*sin(2*pi/n*(n-k))/(cosh(eta_o+j*r1) - cos(2*pi/n*(n-k))), (i+0.5)*dl]\
   for i in range(l) for j in range(r+1) for k in range(n)]
  p1 = len(list_grid_01)
  p2 = p1 + len(list_grid_02)
  p3 = p2 + len(list_grid_03)
  p4 = p3 + len(list_grid_04)
  #20点メッシュ
  list_mesh_01 = [[i*r*n+j*n+k, f(i,j,k,r+1), n+f(i,j,k,r+1), 1+n+f(i,j,k%n,r+1), 1+f(i,j,k%n,r+1), (r+1)*n+f(i,j,k,r+1), (r+1)*n+n+f(i,j,k,r+1), 1+(r+1)*n+n+f(i,j,k%n,r+1), 1+(r+1)*n+f(i,j,k%n,r+1), p2+f(i,j,k,r), p1+n+f(i,j,k,r+1), p2+1+f(i,j,k%n,r), p1+f(i,j,k,r+1), p2+r*n+f(i,j,k,r), p1+n+(r+1)*n+f(i,j,k,r+1), p2+1+r*n+f(i,j,k%n,r), p1+(r+1)*n+f(i,j,k,r+1), p3+f(i,j,k,r+1), p3+n+f(i,j,k,r+1), p3+1+n+f(i,j,k%n,r+1), p3+1+f(i,j,k%n,r+1)]\
   for i in range(l) for j in range(r) for k in range(1,n+1)]
  s1 = len(list_mesh_01)

  #20点要素のリスト
  list_node_01 = [[i*r*n+j*n+k+1,j+r_o+1, k%n, i] for i in range(l) for j in range(r) for k in range(n)]
  return list_grid_01,list_grid_02,list_grid_03,list_grid_04,list_mesh_01,list_node_01,p1,p2,p3,p4,s1

#内管
def inner_grid():
  #内管の各メッシュの角度を求める
  theta_01 = [-sum(phi(list_grid_01[i+r*n-1], list_grid_01[i+r*n], center_01) for i in range(1,j+1)) for j in range(n)]
  theta_02 = [asin(list_grid_02[r*n][1]/length(list_grid_02[r*n], center_01)) if j==0 else\
   asin(list_grid_02[r*n][1]/length(list_grid_02[r*n], center_01))-sum(phi(list_grid_02[i+r*n-1], list_grid_02[i+r*n], center_01) for i in range(1,j+1)) for j in range(n)]

  #座標
  #8点メッシュの座標を作成
  list_grid_05 = [[(Ri-(j+1)*w_i)*cos(theta_01[k]) + center_01[0], (Ri-(j+1)*w_i)*sin(theta_01[k]) + center_01[1], i*dl + center_01[2]]\
   for i in range(l+1) for j in range(r_i) for k in range(n)]
  p5 = p4 + len(list_grid_05)

  #θ方向に隣り合った点の中点
  list_grid_06 = [[(Ri-(j+1)*w_i)*cos(theta_02[k]) + center_01[0], (Ri-(j+1)*w_i)*sin(theta_02[k]) + center_01[1], i*dl + center_01[2]]\
   for i in range(l+1) for j in range(r_i) for k in range(n)]
  p6 = p5 + len(list_grid_06)

  #r方向に隣り合った点の中点
  list_grid_07 = [[(Ri-(j+1)*w_i+w_i/2)*cos(theta_01[k]) + center_01[0], (Ri-(j+1)*w_i+w_i/2)*sin(theta_01[k]) + center_01[1], i*dl + center_01[2]]\
   for i in range(l+1) for j in range(r_i) for k in range(n)]
  p7 = p6 + len(list_grid_07)

  #z方向に隣り合った点の中点
  list_grid_08 = [[(Ri-(j+1)*w_i)*cos(theta_01[k]) + center_01[0], (Ri-(j+1)*w_i)*sin(theta_01[k]) + center_01[1], (i + 0.5)*dl + center_01[2]]\
   for i in range(l) for j in range(r_i) for k in range(n)]
  p8 = p7 + len(list_grid_08)

  #20点メッシュ
  list_mesh_02 = [[i*r*n+k+s1, f(i,0,k,r+1)+r*n, p4+f(i,0,k,r_i), p4+f(i,0,k%n,r_i)+1, f(i,0,k%n,r+1)+1+r*n, f(i,0,k,r+1)+r*n+(r+1)*n, p4+f(i,0,k,r_i)+r_i*n, p4+f(i,0,k%n,r_i)+1+r_i*n, f(i,0,k%n,r+1)+1+r*n+(r+1)*n, p6+f(i,0,k,r_i), p5+f(i,0,k,r_i), p6+f(i,0,k%n,r_i)+1, p1+f(i,0,k,r+1)+r*n, p6+f(i,0,k,r_i)+r_i*n, p5+f(i,0,k,r_i)+r_i*n, p6+f(i,0,k%n,r_i)+1+r_i*n, p1+f(i,0,k,r+1)+r*n+(r+1)*n, p3+f(i,0,k,r+1)+r*n, p7+f(i,0,k,r_i), p7+f(i,0,k%n,r_i)+1, p3+f(i,0,k%n,r+1)+1+r*n]\
   for i in range(l) for k in range(1,n+1)]
  s2 = len(list_mesh_02)

  list_mesh_03 = [[i*r*n+(j-1)*n+k+s1+s2, p4+f(i,j-1,k,r_i), p4+n+f(i,j-1,k,r_i), p4+1+n+f(i,j-1,k%n,r_i), p4+1+f(i,j-1,k%n,r_i), p4+r_i*n+f(i,j-1,k,r_i), p4+r_i*n+n+f(i,j-1,k,r_i), p4+1+r_i*n+n+f(i,j-1,k%n,r_i), p4+1+r_i*n+f(i,j-1,k%n,r_i), p6+f(i,j,k,r_i), p5+n+f(i,j-1,k,r_i), p6+1+f(i,j,k%n,r_i), p5+f(i,j-1,k,r_i), p6+r_i*n+f(i,j,k,r_i), p5+n+r_i*n+f(i,j-1,k,r_i), p6+1+r_i*n+f(i,j,k%n,r_i), p5+r_i*n+f(i,j-1,k,r_i), p7+f(i,j-1,k,r_i), p7+n+f(i,j-1,k,r_i), p7+1+n+f(i,j-1,k%n,r_i), p7+1+f(i,j-1,k%n,r_i)]\
   for i in range(l) for j in range(1,r_i) for k in range(1,n+1)]
  s3 = len(list_mesh_03)

  #20点要素のリスト
  list_node_02 = [[i*r*n+j*n+k+s1+1, r+r_o+1+j, k%n, i] for i in range(l) for j in range(r_i) for k in range(n)]
  return list_grid_05,list_grid_06,list_grid_07,list_grid_08,list_mesh_02,list_mesh_03,list_node_02,p5,p6,p7,p8,s2,s3

#外管
def outer_grid():
  #外管の各メッシュの角度を求める
  theta_03 = [-sum(phi(list_grid_01[i-1], list_grid_01[i], center_02) for i in range(1,j+1)) for j in range(n)]
  theta_04 = [asin(list_grid_02[0][1]/length(list_grid_02[0], center_02)) if j==0 else\
   asin(list_grid_02[0][1]/length(list_grid_02[0], center_02)) - sum(phi(list_grid_02[i-1], list_grid_02[i], center_02) for i in range(1,j+1)) for j in range(n)]

  #座標
  #8点メッシュの座標を作成
  list_grid_09 = [[(Ro+(j+1)*w_o)*cos(theta_03[k]) + center_02[0], (Ro+(j+1)*w_o)*sin(theta_03[k]) + center_02[1], i*dl + center_02[2]]\
   for i in range(l+1) for j in range(r_o) for k in range(n)]
  p9 = p8 + len(list_grid_09)

  #θ方向に隣り合った点の中点
  list_grid_10 = [[(Ro+(j+1)*w_o)*cos(theta_04[k]) + center_02[0], (Ro+(j+1)*w_o)*sin(theta_04[k]) + center_02[1], i*dl + center_02[2]]\
   for i in range(l+1) for j in range(r_o) for k in range(n)]
  p10 = p9 + len(list_grid_10)

  #r方向に隣り合った点の中点
  list_grid_11 = [[(Ro+(j+1)*w_o-w_o/2)*cos(theta_03[k]) + center_02[0], (Ro+(j+1)*w_o-w_o/2)*sin(theta_03[k]) + center_02[1], i*dl + center_02[2]]\
   for i in range(l+1) for j in range(r_o) for k in range(n)]
  p11 = p10 + len(list_grid_11)

  #z方向に隣り合った点の中点
  list_grid_12 = [[(Ro+(j+1)*w_o)*cos(theta_03[k]) + center_02[0], (Ro+(j+1)*w_o)*sin(theta_03[k]) + center_02[1], (i + 0.5)*dl + center_02[2]]\
   for i in range(l) for j in range(r_o) for k in range(n)]
  p12 = p11 + len(list_grid_12)

  #20点メッシュ
  list_mesh_04 = [[i*r*n+k+s1+s2+s3, p8+f(i,0,k,r_o), f(i,0,k,r+1), f(i,0,k%n,r+1)+1, p8+f(i,0,k%n,r_o)+1, p8+f(i,0,k,r_o)+r_o*n, f(i,0,k,r+1)+(r+1)*n, f(i,0,k%n,r+1)+1+(r+1)*n, p8+f(i,0,k%n,r_o)+1+r_o*n, p10+f(i,0,k,r_o), p1+f(i,0,k,r+1), p10+f(i,0,k%n,r_o)+1, p9+f(i,0,k,r_o), p10+f(i,0,k,r_o)+r_o*n, p1+f(i,0,k,r+1)+(r+1)*n, p10+f(i,0,k%n,r_o)+1+r_o*n, p9+f(i,0,k,r_o)+r_o*n, p11+f(i,0,k,r_o), p3+f(i,0,k,r+1), p3+f(i,0,k%n,r+1)+1, p11+f(i,0,k%n,r_o)+1]\
   for i in range(l) for k in range(1,n+1)]
  s4 = len(list_mesh_04)

  list_mesh_05 = [[i*r*n+(j-1)*n+k+s1+s2+s3+s4, p8+f(i,j,k,r_o), p8+f(i,j-1,k,r_o), p8+1+f(i,j-1,k%n,r_o), p8+1+f(i,j,k%n,r_o), p8+f(i,j,k,r_o)+r_o*n, p8+r_o*n+f(i,j-1,k,r_o), p8+1+r_o*n+f(i,j-1,k%n,r_o), p8+1+r_o*n+f(i,j,k%n,r_o), p10+f(i,j,k,r_o), p9+f(i,j-1,k,r_o), p10+1+f(i,j,k%n,r_o), p9+f(i,j,k,r_o), p10+f(i,j,k,r_o)+r_o*n, p9+r_o*n+f(i,j-1,k,r_o), p10+1+r_o*n+f(i,j,k%n,r_o), p9+f(i,j,k,r_o)+r_o*n, p11+f(i,j,k,r_o), p11+f(i,j-1,k,r_o), p11+1+f(i,j-1,k%n,r_o), p11+1+f(i,j,k%n,r_o)]\
   for i in range(l) for j in range(1,r_o) for k in range(n)]
  s5 = len(list_mesh_05)

  #20点要素のリスト
  list_node_03 = [[i*r*n+j*n+k+s1+s2+s3+1, 1+j, k%n, i] for i in range(l) for j in range(r_o) for k in range(n)]
  return list_grid_09,list_grid_10,list_grid_11,list_grid_12,list_mesh_04,list_mesh_05,list_node_03,p9,p10,p11,p12,s4,s5

#流体のメッシュの幅の計測と平行移動量の決定
def width(list_grid, r,n):
  #width = [length(list_grid_01[k], list_grid_01[k+r*n]) for k in range(n)]
  #para = -min(width)+1.0e-6
  para1 = length(list_grid_01[int(n/2)],list_grid_01[int(n/2)+r*n])
  print(para1)
  return para-para1

#流体を外管にめり込ませる
def dig_outer(x,eps):
  center_i = [center_02[0]+Ri+eps-Ro-x,0,0]
  move = [k for k in range(n) if list_grid_01[k][0]<=center_02[0] if (center_i[0]-list_grid_01[k][0])**2+list_grid_01[k][1]**2<=(Ri+eps)**2]
  if len(move)==0: return
  psi  = [-phi(center_02,list_grid_01[move[k]],center_i) if list_grid_01[move[k]][1]<0 else -2*pi + phi(center_02,list_grid_01[move[k]],center_i) for k in range(len(move))]
  psi2 = [-phi(center_02,list_grid_02[move[k]],center_i) if list_grid_02[move[k]][1]<0 else -2*pi + phi(center_02,list_grid_02[move[k]],center_i) for k in range(len(move))]
  for i in range(l+1):
    for k in range(len(move)):
      list_grid_01[move[k]+(r+1)*n*i][0] = (Ri+eps)*cos(psi[k]) + center_i[0]
      list_grid_01[move[k]+(r+1)*n*i][1] = (Ri+eps)*sin(psi[k])
      list_grid_02[move[k]+(r+1)*n*i][0] = (Ri+eps)*cos(psi2[k]) + center_i[0]
      list_grid_02[move[k]+(r+1)*n*i][1] = (Ri+eps)*sin(psi2[k])
  for i in range(l):
    for k in range(len(move)):
      list_grid_04[move[k]+(r+1)*n*i][0] = (list_grid_01[move[k]+(r+1)*n*i][0]+list_grid_01[move[k]+(r+1)*n*(i+1)][0])/2
      list_grid_04[move[k]+(r+1)*n*i][1] = (list_grid_01[move[k]+(r+1)*n*i][1]+list_grid_01[move[k]+(r+1)*n*(i+1)][1])/2
      list_grid_12[move[k]+r_o*n*i][0]   = (list_grid_09[move[k]+r_o*n*i][0]+list_grid_09[move[k]+r_o*n*(i+1)][0])/2
      list_grid_12[move[k]+r_o*n*i][1]   = (list_grid_09[move[k]+r_o*n*i][1]+list_grid_09[move[k]+r_o*n*(i+1)][1])/2
  for k in range(len(move)):
    for i in range(l+1):
      list_grid_11[move[k]+r_o*n*i][0] = (list_grid_01[move[k]+(r+1)*n*i][0] + list_grid_09[move[k]+r_o*n*i][0])/2
      list_grid_11[move[k]+r_o*n*i][1] = (list_grid_01[move[k]+(r+1)*n*i][1] + list_grid_09[move[k]+r_o*n*i][1])/2
  return

#平行移動
def pararell(para):
  for k in range(n):
    for i in range(l+1):
      list_grid_01[k+(r+1)*n*i+r*n][0] = list_grid_01[k+(r+1)*n*i+r*n][0] + para
      list_grid_02[k+(r+1)*n*i+r*n][0] = list_grid_02[k+(r+1)*n*i+r*n][0] + para
    for i in range(l):
      list_grid_04[k+(r+1)*n*i+r*n][0] = list_grid_04[k+(r+1)*n*i+r*n][0] + para
  for k in range(n):
    for i in range(l+1):
      list_grid_03[k+r*n*i][0] = (list_grid_01[k+(r+1)*n*i][0] + list_grid_01[k+(r+1)*n*i+r*n][0])/2
      list_grid_03[k+r*n*i][1] = (list_grid_01[k+(r+1)*n*i][1] + list_grid_01[k+(r+1)*n*i+r*n][1])/2

  for i in range(len(list_grid_05)): list_grid_05[i][0] = list_grid_05[i][0] + para
  for i in range(len(list_grid_06)): list_grid_06[i][0] = list_grid_06[i][0] + para
  for i in range(len(list_grid_07)): list_grid_07[i][0] = list_grid_07[i][0] + para
  for i in range(len(list_grid_08)): list_grid_08[i][0] = list_grid_08[i][0] + para
  return

#paraview用にvtk形式で保存
def exportVtk(filename):
  fileobj = open(filename, "w")

  fileobj.write("# vtk DataFile Version 2.0\n10\nASCII\nDATASET UNSTRUCTURED_GRID\n")
  fileobj.write("POINTS "+str(p12)+" float\n")
  vtk_node(fileobj,list_grid_01)
  vtk_node(fileobj,list_grid_02)
  vtk_node(fileobj,list_grid_03)
  vtk_node(fileobj,list_grid_04)
  vtk_node(fileobj,list_grid_05)
  vtk_node(fileobj,list_grid_06)
  vtk_node(fileobj,list_grid_07)
  vtk_node(fileobj,list_grid_08)
  vtk_node(fileobj,list_grid_09)
  vtk_node(fileobj,list_grid_10)
  vtk_node(fileobj,list_grid_11)
  vtk_node(fileobj,list_grid_12)

  fileobj.write("CELLS "+str(s1+s2+s3+s4+s5)+" "+str((s1+s2+s3+s4+s5)*21)+"\n")
  vtk_mesh(fileobj,list_mesh_01)
  vtk_mesh(fileobj,list_mesh_02)
  vtk_mesh(fileobj,list_mesh_03)
  vtk_mesh(fileobj,list_mesh_04)
  vtk_mesh(fileobj,list_mesh_05)

  fileobj.write("CELL_TYPES "+str(s1+s2+s3+s4+s5)+"\n")
  for i in range(s1+s2+s3+s4+s5):
    fileobj.write("25\n")

  fileobj.write("CELL_DATA "+str(s1+s2+s3+s4+s5)+"\n"+"SCALARS cell_scalars float\n"+"LOOKUP_TABLE default\n")
  for i in range(s1):
    fileobj.write("0\n")
  for i in range(s2+s3):
    fileobj.write("10\n")
  for i in range(s4+s5):
    fileobj.write("20\n")

  fileobj.close()
  return

#abaqus形式で保存
def exportInp(filename):
  fileobj = open(filename, "w")

  fileobj.write("**\n** ABAQUS Input Deck Generated by HyperMesh Version  : 13.0.110.31\n** Generated using HyperMesh-Abaqus Template Version : 13.0.110\n**\n**   Template:  ABAQUS/STANDARD 3D\n**\n*NODE\n")
  inp_node(fileobj,list_grid_01,0)
  inp_node(fileobj,list_grid_02,p1)
  inp_node(fileobj,list_grid_03,p2)
  inp_node(fileobj,list_grid_04,p3)
  inp_node(fileobj,list_grid_05,p4)
  inp_node(fileobj,list_grid_06,p5)
  inp_node(fileobj,list_grid_07,p6)
  inp_node(fileobj,list_grid_08,p7)
  inp_node(fileobj,list_grid_09,p8)
  inp_node(fileobj,list_grid_10,p9)
  inp_node(fileobj,list_grid_11,p10)
  inp_node(fileobj,list_grid_12,p11)

  fileobj.write("*ELEMENT,TYPE=C3D20R,ELSET=component1\n")
  inp_mesh(fileobj,list_mesh_01)

  fileobj.write("*ELEMENT,TYPE=C3D20R,ELSET=component2\n")
  inp_mesh(fileobj,list_mesh_02)
  inp_mesh(fileobj,list_mesh_03)

  fileobj.write("*ELEMENT,TYPE=C3D20R,ELSET=component3\n")
  inp_mesh(fileobj,list_mesh_04)
  inp_mesh(fileobj,list_mesh_05)

  fileobj.close()
  return

#hypermesh形式で保存
def exportFem(filename):
  fileobj = open(filename,"w")
  #fileobj.write("$$\n$$  GRID DATA\n$$\n")
  fem_node(fileobj,list_grid_01,0)
  fem_node(fileobj,list_grid_02,p1)
  fem_node(fileobj,list_grid_03,p2)
  fem_node(fileobj,list_grid_04,p3)
  fem_node(fileobj,list_grid_05,p4)
  fem_node(fileobj,list_grid_06,p5)
  fem_node(fileobj,list_grid_07,p6)
  fem_node(fileobj,list_grid_08,p7)
  fem_node(fileobj,list_grid_09,p8)
  fem_node(fileobj,list_grid_10,p9)
  fem_node(fileobj,list_grid_11,p10)
  fem_node(fileobj,list_grid_12,p11)

  fileobj.write("$\n$  CHEXA Elements: 2nd Order\n$\n")
  fem_mesh(fileobj,change20node(list_mesh_01))
  fem_mesh(fileobj,change20node(list_mesh_02))
  fem_mesh(fileobj,change20node(list_mesh_03))
  fem_mesh(fileobj,change20node(list_mesh_04))
  fem_mesh(fileobj,change20node(list_mesh_05))

  fileobj.write("$\n$HMMOVE        1\n$%15dTHRU%12d\n$\n" %(1,s1))
  if s2>0: fileobj.write("$\n$HMMOVE        2\n$%15dTHRU%12d\n$\n" %(s1+1,s1+s2+s3))
  if s4>0: fileobj.write("$\n$HMMOVE        3\n$%15dTHRU%12d\n$\n" %(s1+s2+s3+1,s1+s2+s3+s4+s5))

  fileobj.write("$HMNAME COMP                   1\"fluid\"\n$HWCOLOR COMP                  1       6\n")
  fileobj.write("$HMNAME COMP                   2\"inner\"\n$HWCOLOR COMP                  2       4\n")
  fileobj.write("$HMNAME COMP                   3\"outer\"\n$HWCOLOR COMP                  3       5\n")
  fileobj.close()
  return

#haskell用にデータを加工
def exportHaskell():
  if r_i>0:
    if r_o>0: data = np.concatenate((list_grid_01,list_grid_02,list_grid_03,list_grid_04,list_grid_05,list_grid_06,list_grid_07,list_grid_08,list_grid_09,list_grid_10,list_grid_11,list_grid_12),axis=0)
    else:     data = np.concatenate((list_grid_01,list_grid_02,list_grid_03,list_grid_04,list_grid_05,list_grid_06,list_grid_07,list_grid_08),axis=0)
  elif r_o>0: data = np.concatenate((list_grid_01,list_grid_02,list_grid_03,list_grid_04,list_grid_09,list_grid_10,list_grid_11,list_grid_12),axis=0)
  else: data = np.concatenate((list_grid_01,list_grid_02,list_grid_03,list_grid_04),axis=0)

  twn_ = np.array(list_mesh_01)
  if s2>0: twn_ = np.concatenate((twn_,list_mesh_02),axis=0)
  if s3>0: twn_ = np.concatenate((twn_,list_mesh_03),axis=0)
  if s4>0: twn_ = np.concatenate((twn_,list_mesh_04),axis=0)
  if s5>0: twn_ = np.concatenate((twn_,list_mesh_05),axis=0)

  indexdata = np.array(list_node_01)
  if len(list_node_02)!=0: indexdata = np.concatenate((indexdata,list_node_02),axis=0)
  if len(list_node_03)!=0: indexdata = np.concatenate((indexdata,list_node_03),axis=0)

  datax = data[:,0]
  datay = data[:,1]
  dataz = data[:,2]

  twn = twn_[:, 1:]
  (row, clm) = twn.shape

  indexnode = indexdata[:,0]
  indexr = indexdata[:,1]
  indextheta = indexdata[:,2]
  indexz = indexdata[:,3]

  numf = max(indexnode)
  numr = max(indexr)
  numt = max(indextheta)+1
  numz = max(indexz)+1

  numbers = np.array([numr,numt,numz])
  arrg = np.ones((numr,numt,numz))

  num = 0
  while num < numf:
      node = indexnode[num]
      r = indexr[num]
      t = indextheta[num]
      z = indexz[num]
      arrg[r-1,t,z]=node
      num += 1

  twn1 = set_twnid(arrg,twn,numr,numt,numz)
  #arrg2 = addcoord(arrg,numr,numt,numz)
  #twn2 = set_twnid(arrg2,twn,numr+2,numt+2,numz+2)
  arrg3 = onlyyz(arrg,numr,numt,numz)
  twn3 = set_twnid(arrg3,twn,numr,numt+2,numz+2)

  data=np.vstack((datax, datay, dataz))
  return data, twn3, twn_, indexdata

if __name__ == '__main__':
  print("innner",r_i)
  print("fluid",r)
  print("outer",r_o)
  list_grid_01,list_grid_02,list_grid_03,list_grid_04,list_mesh_01,list_node_01,p1,p2,p3,p4,s1 = fluid_grid()
  list_grid_05,list_grid_06,list_grid_07,list_grid_08,list_mesh_02,list_mesh_03,list_node_02,p5,p6,p7,p8,s2,s3 = inner_grid()
  list_grid_09,list_grid_10,list_grid_11,list_grid_12,list_mesh_04,list_mesh_05,list_node_03,p9,p10,p11,p12,s4,s5 = outer_grid()

  #para = width(list_grid_01,r,n)
  #pararell(para)
  data, twn3, twn_, indexdata = exportHaskell()
  #外管がめり込んでいない状態の座標出力
  np.savetxt('p_node_old.csv', data.T, delimiter=',')
  np.savetxt('p_node.csv', data.T, delimiter=',')
#  exportInp("export_bipolar_old.inp")

  list_grid_01,list_grid_02,list_grid_03,list_grid_04,list_mesh_01,list_node_01,p1,p2,p3,p4,s1 = fluid_grid()
  list_grid_05,list_grid_06,list_grid_07,list_grid_08,list_mesh_02,list_mesh_03,list_node_02,p5,p6,p7,p8,s2,s3 = inner_grid()
  list_grid_09,list_grid_10,list_grid_11,list_grid_12,list_mesh_04,list_mesh_05,list_node_03,p9,p10,p11,p12,s4,s5 = outer_grid()
  para = width(list_grid_01,r,n)
  dig_outer(dig,0.5e-7)

  #pararell(para-dig)
  width(list_grid_01,r,n)
  data, twn3, twn_, indexdata = exportHaskell()
  np.savetxt('p_numbers.csv', [r_i,r_o,n,l],fmt="%.0f",delimiter=',')
 # np.savetxt('p_node.csv', data.T, delimiter=',')
  np.savetxt('p_twngroup.csv', twn3, fmt="%.0f", delimiter=',')
  np.savetxt('export_grid.csv', data.T, delimiter=',')
  np.savetxt('export_node_number.csv', twn_, fmt="%.0f", delimiter=',')
  np.savetxt('export_list.csv', indexdata, fmt="%.0f", delimiter=',')

  exportVtk("export_bipolar.vtk")
#  exportInp("export_bipolar.inp")
#  exportFem("export_bipolar.fem")
