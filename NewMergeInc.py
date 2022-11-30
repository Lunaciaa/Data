import pandas as pd
import os
import glob


# Khai bao cac bien
path = os.getcwd() + '\INCOME' # lay duong dan cua file nay + '' (trong ngoac la cai thu muc hien tai)
csv_files = glob.glob(os.path.join(path, "*.csv")) # duong dan chi tiet
indexC = []
df = pd.DataFrame()
b = []
c= []
ErrorTicker = []
const = pd.DataFrame()

# Cai index nay de lay toan bo csv co trong file
def index():
    for x in csv_files:
        x = x.split('\\')[-1].split('.')[0]
        indexC.append(x)
    return indexC

# Chay vong lap de lay data

for ticker in index():
    oneUse = pd.DataFrame()
    yearcol = []
    c = []
    try:
        a = pd.read_csv(path + fr'\{ticker}.csv')
        for y in range(0,23):
            yearcol = []
            c = []
            for x in range(1,18): 
                yearcol.append(a.columns[x])
                c.append(a.iloc[y][x])
            d = pd.DataFrame([yearcol,c]).T
            if y == 0:
                oneUse = d
            else:
                oneUse = pd.merge(oneUse, d, on= oneUse.columns[0])
        tickerDataframe = pd.DataFrame([ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker,ticker])
        ghop = pd.merge(tickerDataframe,oneUse, left_index= True, right_index = True) # -> Ghop 2 dataframe lai
        const = pd.concat([const,ghop]) # -> Gop voi file tong
        print(ticker)
    except IndexError:
        ErrorTicker.append(ticker) # -> gom nhung ticker loi vay
        continue
print('Task Completed, try to extract file csv...')
headerlist = []
headerTemp = pd.read_csv(path + fr'\AAA.csv')

for z in range(0,23):
    headerlist.append(headerTemp.iloc[z][0])
headerlist.insert(0, 'Năm')
headerlist = pd.DataFrame([headerlist])
temptickerFirst = pd.DataFrame(['Ticker'])
headerlist = pd.merge(temptickerFirst,headerlist, left_index= True, right_index= True)
const.columns = range(0,25)
headerlist.columns = range(0,25)
const = pd.concat([headerlist,const])
ErrorTicker = pd.DataFrame(ErrorTicker)
ErrorTicker.to_csv('NewErrorTickerInc.csv',encoding='utf-8-sig',index=False, header= False)
const.to_csv('NewIncMetgeData.csv', encoding='utf-8-sig',index=False, header= False)

