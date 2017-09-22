import pandas as pd
import numpy as np

pk  = pd.read_csv('./csv/characteristics.csv',encoding="SHIFT-JIS")
typ = pd.read_csv('./csv/type_list.csv')

# N行目に該当するタイプの相性、数が足りないものは0で埋めた
eff    = pd.read_csv('./csv/type_effective.csv',header = None)
not_so  = pd.read_csv('./csv/type_notso.csv',header = None)
no_dmg = pd.read_csv('./csv/type_0.csv',header=None)

ind = lambda n, df : True if len(df)== n else False
df2list = lambda df : list (map( (lambda arr : list(arr)) , df.values))


#print( character )

#Pokemonの名前を入力するとそのPokemonのタイプを返す
def pokemon_type():
        print(' Input Pokemon you want to search in KATAKANA ')
        indicator = True

        while indicator == True:
            name = str(input())
            search = pk[pk['name'].str.contains(name)]
            indicator = ind(0,search)
            if (indicator == True): print('No hits, please try again')

        while (ind(1,search)==False) :
            print('you mean these Pokemon?')
            search1 = search.loc[:,['number','name']]
            print(search1)
            print('choose a number you want to search')
            number = input() #全角、ハイフン未対応
            search = search1[search1['number'].str.contains(number)]
            if (ind(0,search) == True): print('No hits, please try again')

        print('The type of this Pokemon is...')
        
        print(search.values[0][1:4])
        return search.values[0][1:4]

def pokemon_type_easy(name):
    return pk[pk['name'].str.contains(name)].values[0][1:4]

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

# 表を出力。カナでタイプ受け取り info=[name,type1,type2]
def aisho(info):
    lis1 = type2list(info[1])
    lis2 = type2list(info[2])
    lis = list(map(lambda x,y:x*y ,lis1,lis2))
    marks = [info[0]]
    for i in range(18):
        if   lis[i]== 1.0 : marks += [' ']
        elif lis[i]== 2.0 : marks += ['○']
        elif lis[i]== 4.0 : marks += ['●']
        elif lis[i]== 0.5 : marks += ['▲']
        elif lis[i]== 0.25: marks += ['□']
        elif lis[i]== 0.0 : marks += ['x']
        else :marks +=['erorr']
    return marks

def aishos(infos):
    idx = [['なまえ']+list(typ['kanji'])]
    data = [aisho(infos[i]) for i in range(len(infos))]

    df = pd.DataFrame(idx+data)
    print ( df)
    df.to_csv('test.csv',index=False,header=None,sep=',')



if __name__ == '__main__':



#    print(pokemon_type()[0])
#    print(type2list('ノーマル'))
    #  aishos([['+++','フェアリー',0]])
    # aisho('',[0,'ゴースト'])
    # aisho('',['フェアリー','ゴースト'])

      t1 = pokemon_type_easy('ミミッキュ')
      t2 = pokemon_type_easy('カプ・テテフ')
#    types = pokemon_type_easy('カビゴン')
    #  aisho(t)
      print(t2)
      aishos([t1,t2])
