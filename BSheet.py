import requests
import pandas as pd

# Khai bao bien
a = pd.read_csv('ticker-sort.csv',header= None)
a = a[a.columns[0]].values.tolist()
const = pd.DataFrame()
year = ['2008', '2012', '2016', '2020', '2024']
errorTicker = []
outputErrorBsheet = pd.DataFrame()

# Function lay data ve
def start(ten, year):
    url = f'https://s.cafef.vn/bao-cao-tai-chinh/{ten}/BSheet/{year}/0/0/0/0/bao-cao-tai-chinh-cong-ty-co-phan-nhua-an-phat-xanh.chn'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df1 = df_list[-2]
    df2 = df_list[-1]
    df = pd.concat([df1,df2])
    return df

# Function gop data lai
def merge(ten, year):
    global const 
    if year == '2008':
        const = start(ten, year)
        
    else:
        const['g'] = const.groupby(const.columns[0]).cumcount()
        thisYear = start(ten, year)
        thisYear['g'] = thisYear.groupby(thisYear.columns[0]).cumcount()
        const = pd.merge(const,thisYear, how= 'inner', on = [const.columns[0], 'g']).drop('g',axis=1)

# Xuat file error
def error():
    global outputErrorBsheet
    global errorTicker
    outputErrorBsheet = pd.DataFrame(errorTicker)
    outputErrorBsheet.to_csv('outputError_BSheet.csv', index= False, header=False)


#function main de chay
def main():
    global const
    global errorTicker
    for str in a:
        try:
            for b in year:
                merge(str,b)
            const = const.T.drop_duplicates(keep= False).T
            const.to_csv(f'BSheet\{str}.csv', encoding='utf-8-sig',index=False, header= False)
            const = pd.DataFrame()
            print(str + " Completed")
        except:
            print(str + " Not available, Skipping...")
            errorTicker.append(str)
            continue
        error()
    print('Task Complete')


# Chay function
main()

