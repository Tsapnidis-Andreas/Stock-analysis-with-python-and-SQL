import yfinance as yf
import pandas as pd
import datetime as dt
from datetime import datetime
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

def get_data(stock):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=5*365)).strftime('%Y-%m-%d')
    stock_data = yf.download(stock, start=start_date, end=end_date,interval='1mo')
    stock_data = pd.DataFrame(stock_data)
    data = pd.DataFrame(stock_data['Close'])
    data.columns = ['Close']
    data.index=range(1,len(data)+1)
    return(data)

def get_volatility(stock):
    data=get_data(stock)
    returns=data['Close'] / data['Close'].shift(1)-1
    stock_std=returns.std()
    return(round(stock_std*np.sqrt(12),4))

def get_price(stock):
    data=get_data(stock)
    last_close=data.loc[len(data), 'Close']
    return(round(last_close,2))

def get_risk_free_rate():
    risk_free_rate=get_price('^IRX')/100
    return(risk_free_rate)


def linear_regression(x,y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r = r_value ** 2
    beta = slope
    return (beta, r)

def CAPM_value(market_return,beta,annual_risk_free_rate):
    exp_return=annual_risk_free_rate+(market_return-annual_risk_free_rate)*beta
    return(exp_return)


def saving(df):
    global path
    writer = pd.ExcelWriter(path + 'Performance Analysis.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, header=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(df.columns):
        width = max(df[col].apply(lambda x: len(str(x))).max(), len(df[col]))
        worksheet.set_column(i, i, width)
    writer.close()

def plotting(x,y,stock,t,z):
    df=pd.DataFrame({'S&P500':x,stock:y})
    print(df)
    t.hist(bins=30)
    plt.title('Distribution of monthly returns')
    plt.show()
    plt.savefig(path + 'Distribution of monthly returns.png')
    df.rebase().plot()
    plt.title(stock+' vs the market (normalised plot)')
    plt.savefig(path + stock+' vs the market.png')
    df = pd.DataFrame({'S&P500': t, stock: z})
    print(df)
    df.plot_corr_heatmap()
    plt.title('Correlation Heatmap')
    plt.savefig(path + 'Correlation Heatmap.png')




#INITIALIZE
global path
path=" "
stock=' '
data=pd.DataFrame()
data['market closing prices']=get_data('^gspc')['Close']
data['market returns']=data['market closing prices'] / data['market closing prices'].shift(1)-1
data[stock+' closing prices']=get_data(stock)['Close']
data[stock+' returns']=returns=data[stock+' closing prices'] / data[stock+' closing prices'].shift(1)-1
annual_risk_free_rate=get_risk_free_rate()
monthly_risk_free_rate=(1+annual_risk_free_rate)**(1/12)-1
monthly_risk_free_rate = round(monthly_risk_free_rate, 2)
beta,r=linear_regression(data['market returns'].tail(-1)-monthly_risk_free_rate,data[stock+' returns'].tail(-1)-monthly_risk_free_rate)
market_annualised_return=(1+data['market returns'].mean())**12-1
stock_annualised_return=(1+data[stock+' returns'].mean())**12-1
exp_ret=CAPM_value(market_annualised_return,stock_annualised_return,annual_risk_free_rate)
stock_std=get_volatility(stock)
sharpe_ratio=(stock_annualised_return-annual_risk_free_rate)/stock_std
treynor_ratio=(stock_annualised_return-annual_risk_free_rate)/beta
results=[round(stock_annualised_return*100,2),round(stock_std*100,2),round(beta,2),round(exp_ret*100,2),round(sharpe_ratio,2),round(treynor_ratio,2)]
results=np.array(results)
results=results.T
metrics=['annualised average monthly return %','annualised monthly stadard deviation %','beta (5 year monthly)','expected return based on CAPM %','sharpe ratio','treynor ratio']
df=pd.DataFrame(metrics)
df['value']=results
df.columns=['metric','value']
saving(df)
plotting(data['market closing prices'],data[stock+' closing prices'],stock,data[stock+' returns'],data['market returns'])
print(data['market closing prices'])

