import pandas as pd
import numpy as np
from datetime import datetime as dt
# from functools import reduce

pk  = pd.read_csv('./csv/characteristics.csv',encoding="SHIFT-JIS")
typ = pd.read_csv('./csv/type_list.csv')

# N行目に該当するタイプの相性、数が足りないものは0で埋めた
eff    = pd.read_csv('./csv/type_effective.csv',header = None)
not_so  = pd.read_csv('./csv/type_notso.csv',header = None)
no_dmg = pd.read_csv('./csv/type_0.csv',header=None)

want2serch = pd.read_csv('./input.csv',header=None)
pks = list(map(lambda x:x[0],want2serch.values))


ind = lambda n, df : True if len(df)== n else False
df2list = lambda df : list (map( (lambda arr : list(arr)) , df.values))
id_pk = lambda name : pk.query('name ==  \"'+name+'\" ').values[0]
id_pks= list( map(id_pk,pks))


# タイプを一つ受け取って、それぞれのタイプとの相性を表すリストを返す
def type2list(t_kana):
    base = [1.0 for i in range(18)]
    if type(t_kana)== str :
        # type番号
        num = int(typ[typ['kana'].str.contains(t_kana)].values[0][0])
        # type-1番目にtypeで攻撃しときの相性が格納
        print(num)

        twic_rev = df2list(eff)
        half_rev = df2list(not_so)
        zero_rev = df2list(no_dmg)

        twic = []
        half = []
        zero = []

        for i in range(18):
    # タイプIの技でタイプNumに攻撃したらこうかはばつぐん！ならタイプNumの弱点リストにタイプIを追加
            if num in twic_rev[i]: twic+=[i+1]
            if num in half_rev[i]: half+=[i+1]
            if num in zero_rev[i]: zero+=[i+1]

        print(twic)
        print(half)
        print(zero)
        #  倍率に変換
        for i in range(18):
            if (i+1) in twic : base[i]=base[i]*2
            if (i+1) in half : base[i]=base[i]/2
            if (i+1) in zero : base[i]=base[i]*0
    return base

# 表を出力。カナでタイプ受け取り info=pokemonid
def aisho(info):
    lis1 = type2list(info[2])
    lis2 = type2list(info[3])
    lis = list(map(lambda x,y:x*y ,lis1,lis2))
    marks = [info[1]]
    for i in range(18):
        if   lis[i]== 1.0 : marks += [' ']
        elif lis[i]== 2.0 : marks += ['○']
        elif lis[i]== 4.0 : marks += ['◎']
        elif lis[i]== 0.5 : marks += ['△']
        elif lis[i]== 0.25: marks += ['▲']
        elif lis[i]== 0.0 : marks += ['×']
        else :marks +=['erorr']
    return marks

def diffence_aisho(infos):
    idx = [['なまえ']+list(typ['kanji'])]
    data = [aisho(infos[i]) for i in range(len(infos))]
    df = pd.DataFrame(idx+data)
    print ( df)
    nowtime = dt.now().strftime('%m%d_%H%M%S')
    df.to_csv(nowtime+'.csv',index=False,header=None,sep=',')
    return idx+data


print(diffence_aisho(id_pks))
