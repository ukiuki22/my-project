#7ならべ
#All status keeps as list
#ジョーカーなしパス無限回,エラー処理なし、cp無し、手札公開
from numpy.random import *
from functools import reduce


def ranlen(lis):
  return range(len(lis))

#n個の数字をランダムに均等に分割
def suffle():
  lis  =  [i for i in range(13*4)]
  hand = [[0 for i in range(13*4)] for i in range(3)]
  
  i = 0
  while len(lis)>0:
    a = choice(lis)
    i +=1
    hand[(i%3)][a]=1
    lis.remove(a)
  else: return hand


def full_state():
  row = [1 for i in range(13*4)]
  return [row for i in range(4)] #盤面１つ手札３つ

def init_state():
  row = [1 if i%13==7 else 0 for i in range(1,13*4+1)]
  return [row]+suffle() #盤面１つ手札３つ

def trump(row,mark):
  rowS = row
  base = "A234567891JQK"
  for i in ranlen(row):
    if row[i]==0  : rowS[i]=". "
    if row[i]==1  :  rowS[i] = base[i]+" "
    #optionalな情報は盤面情報の後ろに付け足す
    else : row[i] = str(rowS[i])
  if mark==0 : suit = " C "
  if mark==1 : suit = " D "
  if mark==2 : suit = " H "
  if mark==3 : suit = " S "
  return suit + ": " + reduce(lambda x,y : x+y, rowS) 

def display_f(board):
  for i in range(4):
    print( trump(board[0+13*i:13*(i+1)],i) )

def display(state):
  txt = ["Board","p1","p2","p3"]
  for j in range(4):
    print( " "+txt[j] )
    for i in range(4):
      print( trump(state[j][0+13*i:13*(i+1)],i) )
    print("")

def step(info,state): #盤面の変化を与えるパラメータ[pが出す手札,,]
  for j in range(4):
    state[j][info[j]]=0
    state[0][info[j]]=1
  return state

def remove7(state):
  for j in range(1,4):
    for i in range(4):
      state[j][6+13*i]=0
  return state

#def translate(input)

if __name__ == '__main__':

  print("InitalCondition \n")
  status = init_state()
  display(status)

  print("remove 7 from hands \n")
  status =remove7(status)
  display(status)

  turn = 0
  while any([status[0][i]==0 for i in ranlen(status[0])]) :
    turn += 1
    print("turn"+str(turn)+"\n")
    info = [0]
    info.append(int(input()))
    info.append(int(input()))
    info.append(int(input()))
    status = step(info,status)
    display(status)