import pandas as pd
import matplotlib.pyplot as plt


xlsxPath = '/Users/kiichi/Dropbox/my-project/leaf/20171201_.LINE.xlsx'
# xlsxPath = '/Users/kiichi/Dropbox/my-project/leaf/20171204正しいファイル_.LINE.xlsx'
# xlsxPath = '/Users/kiichi/Dropbox/my-project/yuka/before2.xlsx'
read = lambda name :pd.read_excel(xlsxPath, sheetname=name)

df1 = read('20171201_')# (外気CO2でリーク補正)')
df2 = read('外気CO2')

#外気CO2でリーク補正シートから、CO2Rを含む行を検索し、該当する行番号と、umlのタプルからなるリストを返す
def findCO2R(df):
    columns = df.iloc[:,1]
    result  = []
    for i in range(len(columns)):
        if(str(columns[i]).find('CO2R')!=-1): #CO2Rという文字列が含まれていたら
            head = str(columns[i]).find('-> ')+3
            tail = str(columns[i]).find('uml')-1
            result += [(i,int(str(columns[i])[head:tail]))]
    return result

# print(len(findCO2R(df1)))

# 外気CO2シートから大気CO2濃度のリストを返す
def getAtmCO2(df):
    result = []
    for n in range(6):
        for i in range(2,12):
            result+=[(df.iloc[i,3*n],df.iloc[i,3*n+1])]
    return result

#引数はブロック番号(1~60)
#必要な6個のpho,ciを含む行列をとってくる
def makeSubDataFrame(df,number):
    key = findCO2R(df)
    if (number<len(key)):
        subdf = df.iloc[(key[number][0]-6):(key[number][0])]
    else:
        columns = df.iloc[:,1]
        for i in range(len(columns)):
            if(str(columns[i]).find('CO2 Mixer -> OFF')!=-1):
                last = i
                subdf = df.iloc[(last-6):last]
                # print(subdf)
    newColumns = list(df1.iloc[7])
    addColumns = subdf.rename(columns=dict(zip(subdf.columns,newColumns)))
    # print(addColumns)
    return addColumns


#    計算式
PhoUofunc = lambda       CO2R,CO2S,CO2atm,H2OR,H2OS,fda,CndCO2,Trans: (CO2R-( CO2S - (0.008076*(CO2atm-CO2R)+0.0753)  )*(1000-H2OR)/(1000-H2OS))*fda
Cifunc    = lambda PhoUo,CO2R,CO2S,CO2atm,H2OR,H2OS,fda,CndCO2,Trans:((CndCO2-Trans/2)*CO2S-PhoUo)/(CndCO2+Trans/2)

outputA  = []
outputCi = []

for number in range(1,len(findCO2R(df1))+1):
    subdf = makeSubDataFrame(df1,number)
    # print(subdf)
    # subdf.to_csv(str(number)+'.csv')
    CO2R = list(subdf['CO2R'])
    CO2atm = [getAtmCO2(df2)[number-1][1] for i in range(6)]
    # print(CO2atm)
    H2OR = list(subdf['H2OR'])
    H2OS = list(subdf['H2OS'])
    fda = list(subdf['fda'])
    CndCO2 = list(subdf['CndCO2'])
    Trans = list(subdf['Trans'])
    CO2S = list(subdf['CO2S'])
    PhoUo = list(map(PhoUofunc   ,CO2R,CO2S,CO2atm,H2OR,H2OS,fda,CndCO2,Trans))
    Ci    = list(map(Cifunc,PhoUo,CO2R,CO2S,CO2atm,H2OR,H2OS,fda,CndCO2,Trans))

    # print(number)
    print(PhoUo)
    print(Ci)
    outputA  += [sum(PhoUo)/len(PhoUo)]
    outputCi += [sum(Ci)/len(PhoUo)]

forplot = pd.DataFrame([outputA,outputCi],index=['A','Ci'])
# print(forplot)
forplot.to_csv('output.csv')

plt.scatter(outputCi,outputA)
plt.show()


# subdf.to_csv('test.csv')

# print(CO2R,CO2S,CO2atm,H2OR,H2OS,fda,CndCO2,Trans)
# print()

# print(CO2R,CO2S,CO2atm,H2OR,H2OS,fda,CndCO2,Trans)


# print(CO2R)
# CO2atom =
#
# H2OR = getQuantityList('H2OR')
# H2OS = getQuantityList('H2OS')
#
# fda = getQuantityList('fda')
# CndCO2 = getQuantityList('CndCO2')
# CO2R = getQuantityList('CO2R')
# CO2R = getQuantityList('CO2R')
# CO2R = getQuantityList('CO2R')
# CO2R = getQuantityList('CO2R')
#


# df1.iloc[7]
# df1.columns
# print(key[1][0]-1)
# df1.iloc[]

# CO2R が区切り目
# 2番目以降の　Flow: Fixed は必要ないので消す
# CO2Rを手がかりに各ブロックに分ける。
# 各ブロックにはAとCiが一つづつ対応していて、AとCiはある時刻でpho,ciの平均の値。＊最後から6個だけ
# pho,ciはおんどとりからでてくるブロック全体では一定の値と各時刻で変化するいくつかのパラメタの関数
# 全ブロックで(A,Ci)のデータをとったのち、散布図を作る（横軸Ci）

#列1から　Remark=


# print(getAtmCO2(df2))
# print(len(getAtmCO2(df2)))

# print(find_CO2R(df))
# df[df['Unnamed: 1'] == 'Remark=09:39:43 Launched AutoProg /User/Configs/AutoProgs/AutoLog2']
# data1[data1['OPEN 6.3'] == 'Remark=']
# data1.columns
