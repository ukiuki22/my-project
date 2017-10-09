import prettytable

if __name__ == '__main__':
    # CSV ファイルを開く
    path = '/Users/kiichi/Dropbox/my-project/pokemon/1007_140638/2_1.csv'
    # path = './testModel2/1_2.csv'
    fp = open(path, 'r')
    # テーブルを CSV から読み込む
    table = prettytable.from_csv(fp)
    # テーブルを標準出力に書き出す
    print (table)
