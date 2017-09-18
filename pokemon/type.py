import pandas as pd
import numpy as np

pk = pd.read_csv('./csv/characteristics.csv',encoding="SHIFT-JIS")

ind = lambda n, df : True if len(df)== n else False

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

        print('you mean these Pokemon?')
        print(search.loc[:,['number','name']])

        while (ind(1,search)==False) :
            print('choose a number you want to search')
            number = input() #全角、ハイフン未対応
            search = pk[pk['number'].str.contains(number)]
            if (ind(0,search) == True): print('No hits, please try again')

        print('The type of this Pokemon is...')
        print(search.values[0][1:4])
        return (search.values[0][3],search.values[0][4])

# タイプを一つ受け取って、それぞれのタイプとの相性を表すリストを返す
def type2list(t):
    return 




if __name__ == '__main__':
    pokemon_type()




        # 検索が複数ヒットした場合、番号と名前を表示
        # 番号を入力（全角でおk）
        # ヒットしなかった場合やりなおし
        # ひとつに絞れたらタイプを表示
