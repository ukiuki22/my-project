import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from datetime import datetime as dt
from functools import reduce
from itertools import combinations,product

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
        if type(output[3])==str:  return output
        else:
            output[3]='no'
            return output
    w2s = list(map(lambda x:x[0],pd.read_csv(path,header=None,comment='#').values))
    return list( map( id_pk, w2s) )

ind     = lambda n, df   : True if len(df)== n else False
df2list = lambda df      : list (map( (lambda arr : list(arr)) , df.values))
types   = lambda pokemon : (pokemon[2],pokemon[3])
name    = lambda pokemon : pokemon[1]
base_st = lambda pokemon : pokemon[7:13]
ranlen  = lambda lis     : range(len(lis))
judge   = lambda n,lis   : list (map(  (lambda n: n>0 ) ,lis))
trues   = lambda lis     : reduce(lambda x,y:x+y, list(map(lambda a : 1 if a==True else 0, lis)))
comb    = lambda lis,n   : list(list(map(list,list(combinations(lis,n)))))
# want2use menbers , standby menbars から　考えられる全ての組み合わせを出力
jointPTNs = lambda lis1,lis2,n1,n2 :list( map( lambda tap: tap[0]+tap[1],list(product(comb(lis1,n1),comb(lis2,n2)))))
# タイプの情報
typ = pd.read_csv('./csv/type_list.csv')
# N行目に該当するタイプの相性、数が足りないものは0で埋めた
eff    = pd.read_csv('./csv/type_effective.csv',header = None)
not_so  = pd.read_csv('./csv/type_notso.csv',header = None)
no_dmg = pd.read_csv('./csv/type_0.csv',header=None)
# ターゲットとなるポケモンの名前
want2use = pks('./want2use.csv') #pks('./want2use.csv')
top20    = pks('./top20_s6.csv')
standby  = pks('./standby.csv')
party = lambda n :pks('./party'+str(n)+'.csv')

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
def export_deffence_aisho(PT,time,coutions,i):
    # 表を出力。カナでタイプ受け取り info=pokemonid
    def dfc_aisho(pokemon):
        lis1 = dfc_type2list(pokemon[2])
        lis2 = dfc_type2list(pokemon[3])
        lis = list(map(lambda x,y:x*y ,lis1,lis2))
        marks = [pokemon[1]]
        for i in range(18):
            if   lis[i]== 1.0 : marks += ['-']
            elif lis[i]== 2.0 : marks += ['○']
            elif lis[i]== 4.0 : marks += ['◎']
            elif lis[i]== 0.5 : marks += ['△']
            elif lis[i]== 0.25: marks += ['▲']
            elif lis[i]== 0.0 : marks += ['×']
            else :marks +=['erorr']
        return marks
    idx = [['なまえ']+list(typ['kanji'])[:-1]]
    data = [dfc_aisho(PT[i]) for i in ranlen(PT)]
    # print(dfc_aisho(infos[0]))
    df = pd.DataFrame(idx+data)
    # print ( df)
    nowtime = dt.now().strftime('%m%d_%H%M%S')
    df.to_csv(time+'/'+str(coutions)+'_'+str(i)+'_aisho.csv',index=False,header=None,sep=',')#,encoding='shift_jis')
    return idx+data

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
def evaled_df_by_type(pokemon1s,pokemon2s):
        eval_list = [[eval_by_type(pokemon1s[i],pokemon2s[j]) for i in ranlen(pokemon1s) ]for j in ranlen(pokemon2s)]
        idx = [name(pokemon2s[i]) for i in ranlen(pokemon2s)]
        col = [name(pokemon1s[i]) for i in ranlen(pokemon1s)]
        return pd.DataFrame(eval_list,index=idx,columns=col)



#ダメージ倍率 こうかが大きい方を選択
def type_coefficient(pokemon1,pokemon2):

    zipWith_ = lambda a : [a[0][i]*a[1][i] for i in range(len(a[0]))]
    # 自ポケ受け相性のリスト、タイプ番号
    # dfc1 = zipWith_( list( map(dfc_type2list,types(pokemon1))) ) + [1.0]
    num1 = [(typ[typ['kana'].str.contains(types(pokemon1)[i])].values[0][0]) for i in range(2)]
    # 敵ポケ受け相性のリスト、タイプ番号
    dfc2 = zipWith_( list( map(dfc_type2list,types(pokemon2))) ) + [1.0]
    # num2 = [(typ[typ['kana'].str.contains(types(pokemon2)[i])].values[0][0]) for i in range(2)]
    # chem21 = (dfc1[num2[0]-1],dfc1[num2[1]-1])
    chem12 = (dfc2[num1[0]-1],dfc2[num1[1]-1])
    # print('vvv')
    # print(chem12)
    return  max(chem12[0],chem12[1]) #,chem21[0],chem21[1]) #dfc2[num1[0]],dfc2[num1[1]],dfc1[num2[0]],dfc1[num2[1]])#_type2list(types(pokemon1)[0])

"""
ダメージ評価 g(攻,守)=(お互いレベル50、タイプ一致威力100乱数85で攻撃した時、守に与えるダメージ)／守のHP
→（攻撃する側から見たら）1回でHPのどれくらいを削れるか
→（防御する側から見たら）耐えれるターンの逆数
＊性格補正なし
＊理想個体、努力値全振り

与えるダメージ
={（攻撃側のレベル × 2 ÷ 5 ＋ 2）× 技の威力 × 攻撃側の能力値 ÷ 防御側の能力値 ÷ 50 ＋ 2}
×乱数（85～100）÷ 100 ×タイプ一致×タイプ相性1×タイプ相性2

HPの能力値
=（種族値*2+個体値+努力値/4)*レベル/100+レベル+10
HP以外の能力値
={(種族値*2+個体値+努力値/4)*レベル/100+5}*性格補正
"""
dmg  = lambda atk1,def2,typ12,power : ( 22* power * atk1 / def2 / 50 + 2 ) * 0.85 * 1.5 * typ12
abt  = lambda x,hp,eV : (2*x+31+eV/4)*0.5+5*(1+hp)
eval_g = lambda b_atk1, b_def2, b_hp2, typ12 : dmg(abt(b_atk1,0,252),abt(b_def2,0,252),typ12,100)/abt(b_hp2,1,252)
sp_cor = lambda b_sp1,b_sp2,mimikkyu : (1+mimikkyu) if(b_sp1>b_sp2) else mimikkyu

"""
ポケモン相性評価関数f…お互い攻撃しあったときに自分が瀕死になる前に同じ相手を何匹倒せるかの目安
＝  f(自分,相手)
＝　1回で相手を削る割合　＊（　生き残るターン数　＋　すばやさ補正　(0 or 1) + ミミッキュ　）
＝　g(自分,相手)＊(1/g(相手,自分)+d(自分,相手))
＊複数タイプの場合、gが大きくなる方を選ぶ
＊物理、特殊どちらでも計算をしてgが大きくなる方を選ぶ
"""
def eval_function(pokemon1,pokemon2):
    h1,a1,b1,c1,d1,s1 = base_st(pokemon1)
    h2,a2,b2,c2,d2,s2 = base_st(pokemon2)
    typ12 = type_coefficient(pokemon1,pokemon2)
    typ21 = type_coefficient(pokemon2,pokemon1)

    is_mimikkyu = lambda pokemon : 1 if(name(pokemon)=='ミミッキュ') else 0

    mimi1 = is_mimikkyu(pokemon1)
    mimi2 = is_mimikkyu(pokemon2)

    fp1 = eval_g(a1,b2,h2,typ12)*(1/eval_g(a2,b1,h1,typ21) + sp_cor(s1,s2,mimi1) )
    fs1 = eval_g(c1,d2,h2,typ12)*(1/eval_g(c2,d1,h1,typ21) + sp_cor(s1,s2,mimi1) )
    fp2 = eval_g(a2,b1,h1,typ21)*(1/eval_g(a1,b2,h2,typ12) + sp_cor(s2,s1,mimi2) )
    fs2 = eval_g(c2,d1,h1,typ21)*(1/eval_g(c1,d2,h2,typ12) + sp_cor(s2,s1,mimi2) )
    # print(typ12)
    # print(mimi1)
    # print(eval_g(a1,b2,h2,typ12))
    # print(eval_g(c1,d2,h2,typ12))
    # print(sp_cor(s1,s2,mimi1))
    # print(fp)
    # print(fs)
    # print('---')
    return math.ceil((max(fp1,fs1)-max(fp2,fs2))/(max(fp1,fs1)+max(fp2,fs2))*5+5)

def evaled_df(pokemon1s,pokemon2s):
        eval_list = [[eval_function(pokemon1s[i],pokemon2s[j]) for i in ranlen(pokemon1s) ]for j in ranlen(pokemon2s)]
        idx = [name(pokemon2s[i]) for i in ranlen(pokemon2s)]
        col = [name(pokemon1s[i]) for i in ranlen(pokemon1s)]
        return pd.DataFrame(eval_list,index=idx,columns=col)


# 環境に対するパーティーの評価　
def eval_PT(PT,Env):
    df = evaled_df(PT,Env)
    caution = df.where(df<=7).dropna().index
    PTmenber = reduce(lambda x,y: x+','+y ,list( map( lambda arr: list(arr)[1],PT)))
    # print(PTmenber)
    # print(list( map( lambda arr: list(arr)[1],PT)))
    # return (len(caution),list(caution),PTmenber)
    return (len(caution),PTmenber,list(caution),PT) #実際に処理するとき


# if __name__ == '__main__':
#     #hapinasu de hikaku
#     print(party(2)[0][2:13])
#     print(eval_function(party(2)[0],party(2)[1]))
#     print(party(2)[1][2:13])
#     print(eval_function(party(2)[1],party(2)[0]))
#     print(evaled_df(party(2),party(2)))
#     # print(evaled_df_by_type(party(1),[top20[0]]))


# Eval_PTの結果のリストを引数にとり、敵の数が少ない順に並び替え、不利な敵がN個以下のPTの評価表を出力

if __name__ == '__main__':
    allPattarns = jointPTNs(party(4),party(1),0,6)
    coutions=30

    nowtime = dt.now().strftime('%m%d_%H%M%S')
    os.mkdir(nowtime)
    f = open(nowtime+'/partyAnalysis.txt', 'w') # 書き込みモードで開く
    f.write('# -*- coding: utf-8 -*-\n')
    j = 0
    for i in ranlen(allPattarns):

        Evaled = eval_PT(allPattarns[i],top20)
        if Evaled[0]<= coutions:
            print(str(i+1)+'/'+str(len(allPattarns))+'...!')
            j = j + 1
            evaled_df(allPattarns[i],top20).to_csv(nowtime+'/'+str(Evaled[0])+'_'+str(j)+'.csv',sep=',')#,encoding='shift_jis')
            export_deffence_aisho(allPattarns[i],nowtime,Evaled[0],j)
            f.write(str(j)+'--'+str(Evaled[:3])+'\n')
        else:
            print(str(i+1)+'/'+str(len(allPattarns)))
    f.close()
    export_deffence_aisho(party(1),nowtime,'all',0)
