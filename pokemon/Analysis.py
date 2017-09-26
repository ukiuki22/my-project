import pandas as pd
import numpy as np
from datetime import datetime as dt
# from functools import reduce

# 各ポケモンの情報を読み込み、タイプの情報
pk  = pd.read_csv('./csv/characteristics.csv',encoding="SHIFT-JIS")
typ = pd.read_csv('./csv/type_list.csv')

# N行目に該当するタイプの相性、数が足りないものは0で埋めた
eff    = pd.read_csv('./csv/type_effective.csv',header = None)
not_so  = pd.read_csv('./csv/type_notso.csv',header = None)
no_dmg = pd.read_csv('./csv/type_0.csv',header=None)

# サーチしたいポケモンたち
want2serch = pd.read_csv('./input.csv',header=None)
search_pks = list(map(lambda x:x[0],want2serch.values))


ind = lambda n, df : True if len(df)== n else False
df2list = lambda df : list (map( (lambda arr : list(arr)) , df.values))

def id_pk(name) :
    output = pk.query('name ==  \"'+name+'\" ').values[0]
    if type(output[3])==str:
        return output
    else: # たんタイプならば
        output[3]='no'
        return output

# サーチしたいポケモンの全情報
id_pks= list( map(id_pk,search_pks))

print(id_pks)

def atk_type2list(t_kana):
    base = [1.0 for i in range(18)]
    if type(t_kana)== str :
        num = int(typ[typ['kana'].str.contains(t_kana)].values[0][0])
        twic = list(eff.values[num-1]) #.remove(0)
        print(twic)
        half = list(not_so.values[num-1]) #.remove(0)
        zero = list(no_dmg.values[num-1])#.remove(0)
        #  倍率に変換
        for i in range(18):
            if (i+1) in twic : base[i]=base[i]*2
            elif (i+1) in half : base[i]=base[i]/2
            elif (i+1) in zero : base[i]=base[i]*0
    else :
         print(t_kana+'NOT FOUND')
    return base

# タイプを一つ受け取って、それぞれのタイプとの相性を表すリストを返す
def dfc_type2list(t_kana):
    base = [1.0 for i in range(18)]
    if t_kana != 'no' :
        # type番号
        num = int(typ[typ['kana'].str.contains(t_kana)].values[0][0])
        # type-1番目にtypeで攻撃しときの相性が格納
        # print(num)

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

        # print(twic)
        # print(half)
        # print(zero)
        #  倍率に変換
        for i in range(18):
            if (i+1) in twic : base[i]=base[i]*2
            if (i+1) in half : base[i]=base[i]/2
            if (i+1) in zero : base[i]=base[i]*0
    return base

print(dfc_type2list('no'))

# 表を出力。カナでタイプ受け取り info=pokemonid
def dfc_aisho(info):
    lis1 = dfc_type2list(info[2])
    lis2 = dfc_type2list(info[3])
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

# csv出力
def export_diffence_aisho(infos):
    idx = [['なまえ']+list(typ['kanji'])]
    data = [dfc_aisho(infos[i]) for i in range(len(infos))]
    df = pd.DataFrame(idx+data)
    print ( df)
    nowtime = dt.now().strftime('%m%d_%H%M%S')
    df.to_csv(nowtime+'.csv',index=False,header=None,sep=',')
    return idx+data


# 自分と相手のポケモンを選んでタイプ相性で評価
def eval_by_type(pokemon1,pokemon2):
    types = lambda pokemon : (pokemon[2],pokemon[3])
    name = lambda pokemon : pokemon[1]

    zipWith_ = lambda a : [a[0][i]*a[1][i] for i in range(len(a[0]))]
    # 自ポケ受け相性のリスト、タイプ番号
    dfc1 = zipWith_( list( map(dfc_type2list,types(pokemon1))) ) + [1.0,1.0]
    num1 = [(typ[typ['kana'].str.contains(types(pokemon1)[i])].values[0][0]) for i in range(2)]
    # 敵ポケ受け相性のリスト、タイプ番号 NOTE:t単タイプのときバグが発生するかも↓
    dfc2 = zipWith_( list( map(dfc_type2list,types(pokemon2))) ) + [1.0,1.0]
    num2 = [(typ[typ['kana'].str.contains(types(pokemon2)[i])].values[0][0]) for i in range(2)]

    print('dfc1')
    print(dfc1[18])
    print(num2)
    # 相手のtype1,type2の技で攻撃された時のそれぞれの相性
    chem21 = (dfc1[num2[0]],dfc1[num2[1]])
    chem12 = (dfc2[num1[0]],dfc2[num1[1]])
    # 評価関数
    eval_type = lambda a,b,c,d : np.log2(a*b/c/d)

    print(name(pokemon1),name(pokemon2))
    print(chem12,chem21)

    return  eval_type(dfc2[num1[0]],dfc2[num1[1]],dfc1[num2[0]],dfc1[num2[1]])#_type2list(types(pokemon1)[0])

if __name__ == '__main__':
    print(eval_by_type(id_pks[2],id_pks[4]))

    # print(id_pks[2])
