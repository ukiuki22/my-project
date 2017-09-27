import pandas as pd
import numpy as np
from datetime import datetime as dt
from functools import reduce

# 各ポケモンの情報を読み込み
pk  = pd.read_csv('./csv/characteristics.csv',encoding="SHIFT-JIS")

# Pathを入力　全情報をリストで出力 id_pks
def pks(path):
    def id_pk(name) :
        try :
            output = pk.query('name ==  \"'+name+'\" ').values[0]
        except :
            print('Erorr :The name '+name+' is NOT found')
            search = pk[pk['name'].str.contains(name)]
            print('you mean these Pokemon?')
            search1 = search.loc[:,['name']]
            print(search1)
            # print(search1)
            # print('choose a number you want to search')
            # number = input() #全角、ハイフン未対応
            # name = pk.loc[number,['name']]
            # print(name)
            # output = pk.query('name ==  \"'+name+'\" ').values[0]

        if type(output[3])==str:  return output
        # たんタイプならば
        else:
            output[3]='no'
            return output
    w2s = list(map(lambda x:x[0],pd.read_csv(path,header=None).values))
    return list( map( id_pk, w2s) )

ind     = lambda n, df   : True if len(df)== n else False
df2list = lambda df      : list (map( (lambda arr : list(arr)) , df.values))
types   = lambda pokemon : (pokemon[2],pokemon[3])
name    = lambda pokemon : pokemon[1]
ranlen  = lambda lis     : range(len(lis))
judge   = lambda n,lis   : list (map(  (lambda n: n>0 ) ,lis))
trues   = lambda lis     : reduce(lambda x,y:x+y, list(map(lambda a : 1 if a==True else 0, lis)))
# タイプの情報
typ = pd.read_csv('./csv/type_list.csv')
# N行目に該当するタイプの相性、数が足りないものは0で埋めた
eff    = pd.read_csv('./csv/type_effective.csv',header = None)
not_so  = pd.read_csv('./csv/type_notso.csv',header = None)
no_dmg = pd.read_csv('./csv/type_0.csv',header=None)
# ターゲットとなるポケモンの名前
want2use = pks('./want2use.csv')
top20    = pks('./top20_s6.csv')
standby  = pks('./standby.csv')

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

# dfc_type2list('フェアリー')
# dfc_type2list('ゴースト')
# csv出力
def export_diffence_aisho(infos):
    # 表を出力。カナでタイプ受け取り info=pokemonid
    def dfc_aisho(info):
        lis1 = dfc_type2list(info[2])
        lis2 = dfc_type2list(info[3])
        lis = list(map(lambda x,y:x*y ,lis1,lis2))
        marks = [info[1]]
        for i in range(18):
            if   lis[i]== 1.0 : marks += ['-']
            elif lis[i]== 2.0 : marks += ['○']
            elif lis[i]== 4.0 : marks += ['◎']
            elif lis[i]== 0.5 : marks += ['△']
            elif lis[i]== 0.25: marks += ['▲']
            elif lis[i]== 0.0 : marks += ['×']
            else :marks +=['erorr']
        return marks
    idx = [['なまえ']+list(typ['kanji'])]
    data = [dfc_aisho(infos[i]) for i in range(len(infos))]
    # print(dfc_aisho(infos[0]))
    df = pd.DataFrame(idx+data)
    print ( df)
    nowtime = dt.now().strftime('%m%d_%H%M%S')
    df.to_csv(nowtime+'.csv',index=False,header=None,sep=',')
    return idx+data

# export_diffence_aisho([top20[0]])


# 自分と相手のポケモンを選んでタイプ相性で評価
def eval_by_type(pokemon1,pokemon2):

    zipWith_ = lambda a : [a[0][i]*a[1][i] for i in range(len(a[0]))]
    # 自ポケ受け相性のリスト、タイプ番号
    dfc1 = zipWith_( list( map(dfc_type2list,types(pokemon1))) ) + [1.0]
    num1 = [(typ[typ['kana'].str.contains(types(pokemon1)[i])].values[0][0]) for i in range(2)]
    # 敵ポケ受け相性のリスト、タイプ番号
    dfc2 = zipWith_( list( map(dfc_type2list,types(pokemon2))) ) + [1.0]
    num2 = [(typ[typ['kana'].str.contains(types(pokemon2)[i])].values[0][0]) for i in range(2)]

    # print('dfc1')
    # print(dfc1)
    # print(dfc2)
    # print(num1)
    # print(num2)
    # 相手のtype1,type2の技で攻撃された時のそれぞれの相性
    chem21 = (dfc1[num2[0]-1],dfc1[num2[1]-1])
    chem12 = (dfc2[num1[0]-1],dfc2[num1[1]-1])
    # 評価関数
    def eval_type(a,b,c,d) :
        if a == 0 : a = 2**(-3)
        if b == 0 : b = 2**(-3)
        if c == 0 : c = 2**(-3)
        if d == 0 : d = 2**(-3)
        return np.log2(a*b/c/d)

    # print(name(pokemon1),name(pokemon2))
    # print(chem12,chem21)

    return  eval_type(chem12[0],chem12[1],chem21[0],chem21[1]) #dfc2[num1[0]],dfc2[num1[1]],dfc1[num2[0]],dfc1[num2[1]])#_type2list(types(pokemon1)[0])

#  PTポケモンと仮想敵ポケモンのタイプ評価リスト
def evaled_df(pokemon1s,pokemon2s):
        eval_list = [[eval_by_type(pokemon1s[i],pokemon2s[j]) for i in ranlen(pokemon1s) ]for j in ranlen(pokemon2s)]
        idx = [name(pokemon2s[i]) for i in ranlen(pokemon2s)]
        col = [name(pokemon1s[i]) for i in ranlen(pokemon1s)]
        return pd.DataFrame(eval_list,index=idx,columns=col)

# 環境に対するパーティーの評価　返り値はIntで任意のPT内ポケモンでeval<0となった敵の数(=相性がどのポケモンでも有利にならない敵の数)
# 任意の敵にたいしてeval>0となるポケモンが少なくとも1匹以上いればOK
def eval_PT(PT,Env):
    df = evaled_df(PT,Env)
    print(df.where(df<=0))
    lis = df2list(df)
    judges=trues([any(judge(0,lis[i])) for i in ranlen(lis)])
    # print(judges)
    return df.where(df<=0).dropna().index #len(lis)-judges

if __name__ == '__main__':
    a = eval_PT(standby,top20)
    print(a)



    # export_diffence_aisho([top20[0],standby[0]])
    # nowtime = dt.now().strftime('%m%d_%H%M%S')
    # df.to_csv(nowtime+'.csv',sep=',')
