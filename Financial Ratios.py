import yfinance
import pandas as pd
import datetime as dt
from datetime import datetime
import numpy as np
import pyodbc

def get_balance_sheet_data(ticker):
    balance_sheet = ticker.quarterly_balance_sheet
    balance_sheet = pd.DataFrame(balance_sheet.iloc[:, 0])
    print(balance_sheet)
    balance_sheet.to_excel(path + 'bs.xlsx')
    balance_sheet.columns = ['Values']
    balance_sheet.to_excel('balance sheet.xlsx')

    current_assets = balance_sheet.loc['Current Assets', 'Values']
    current_assets2=balance_sheet.loc['Receivables','Values']+balance_sheet.loc['Cash Cash Equivalents And Short Term Investments','Values']
    current_liabilities = balance_sheet.loc['Current Liabilities', 'Values']
    inventory = balance_sheet.loc['Inventory', 'Values']
    debt = balance_sheet.loc['Total Debt', 'Values']
    equity = balance_sheet.loc['Stockholders Equity', 'Values']
    total_assets = balance_sheet.loc['Total Assets', 'Values']
    invested_capital=balance_sheet.loc['Invested Capital', 'Values']
    return(current_assets,current_assets2,current_liabilities,inventory,debt,equity,total_assets,invested_capital)

def get_income_statement_data(ticker):
    yincome_statement = ticker.income_stmt
    yincome_statement = pd.DataFrame(yincome_statement.iloc[:, 0])
    qincome_statement = ticker.quarterly_income_stmt
    qincome_statement = pd.DataFrame(qincome_statement.iloc[:, 0])
    qincome_statement.to_excel(path+'income statement.xlsx')
    yincome_statement.columns = ['Values']
    qincome_statement.columns = ['Values']
    sales = yincome_statement.loc['Operating Revenue', 'Values']
    gross_profit = yincome_statement.loc['Gross Profit', 'Values']
    earnings_per_share = yincome_statement.loc['Basic EPS', 'Values']
    net_income=yincome_statement.loc['Net Income', 'Values']
    return(sales,gross_profit,earnings_per_share,net_income)

def get_dividend_data(ticker):
    data = pd.DataFrame(ticker.get_dividends())['Dividends']
    dividends=data.tolist()
    dividend=dividends[-1]
    return(dividend)
def calculate_ratios(current_assets,current_assets2,current_liabilities,inventory,debt,equity,total_assets,invested_capital,sales,gross_profit,earnings_per_share,net_income,price):
    print('hello')
    current_ratio=current_assets/current_liabilities
    print(inventory)
    quick_ratio=current_assets2/current_liabilities
    print(current_assets)
    print(current_liabilities)
    gross_profit_ratio=gross_profit/sales
    asset_turnover_ratio=sales/total_assets
    debt_to_equity=debt/equity
    pe=price/earnings_per_share
    roi=(net_income/invested_capital)
    b=1-(dividend/earnings_per_share)
    growth_rate=roi*b
    return(current_ratio,quick_ratio,gross_profit_ratio,asset_turnover_ratio,debt_to_equity,pe,growth_rate)

def get_market_data(ticker):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=365*5)).strftime('%Y-%m-%d')
    stock_data = yfinance.download(ticker, start=start_date, end=end_date, interval='1mo')
    stock_data = pd.DataFrame(stock_data)
    stock_data.index=range(1,len(stock_data)+1)
    i=len(stock_data['Close'])
    last_closing_price=stock_data.loc[i,'Close']
    stock_data['returns']=(stock_data['Adj Close']-stock_data['Adj Close'].shift(1))/stock_data['Adj Close'].shift(1)
    avg_return=stock_data['returns'].mean()
    annualised_return=(1+avg_return)**12-1
    return(stock_data['returns'].tail(-1),last_closing_price,annualised_return)

def saving(df):
    df['value']=round(df['value'],2)
    writer = pd.ExcelWriter(path + 'Analysis.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, header=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(df.columns):
        width = max(df[col].apply(lambda x: len(str(x))).max(), len(df[col]))
        worksheet.set_column(i, i, width)
    writer.close()

def saving_SQL(stock_name,current_ratio, quick_ratio, gross_profit_ratio, asset_turnover_ratio, debt_to_equity, pe, growth_rate):
    conn=pyodbc.connect('Driver={SQL Server};' 'Server=LAPTOP-A4REIRQU;' 'Database=practice;' 'Trusted_connection=yes')
    conn.execute('INSERT INTO stock_data (stock_ticker,current_ratio,quick_ratio,gross_profit_margin,asset_turnover,debt_to_equity,PE,growth_rate) VALUES(?,?,?,?,?,?,?,?)',(stock_name,current_ratio, quick_ratio, gross_profit_ratio, asset_turnover_ratio, debt_to_equity, pe, growth_rate))
    conn.commit()
    conn.close()





# INITIALIZING
global path
path=" "
stock_name=' '
ticker=yfinance.Ticker(stock_name)
current_assets,current_assets2,current_liabilities,inventory,debt,equity,total_assets,invested_capital=get_balance_sheet_data(ticker)
sales,gross_profit,earnings_per_share,net_income=get_income_statement_data(ticker)
dividend=get_dividend_data(ticker)
stock_monthly_returns,stock_price,stock_annualised_return=get_market_data(stock_name)
current_ratio,quick_ratio,gross_profit_ratio,asset_turnover_ratio,debt_to_equity,pe,growth_rate=calculate_ratios(current_assets,current_assets2,current_liabilities,inventory,debt,equity,total_assets,invested_capital,sales,gross_profit,earnings_per_share,net_income,stock_price)
results=[current_ratio,quick_ratio,gross_profit_ratio,asset_turnover_ratio,debt_to_equity,pe,growth_rate]
for i in results:
    i='{:f}'.format(i)
results=np.array(results)
results=results.T
metrics=['current ratio','quick ratio','gross profit margin','asset turnover','debt to equity','P/E','growth rate']
df=pd.DataFrame(metrics)
df['value']=results
df.columns=['metric','value']
saving(df)
print(df)
saving_SQL(stock_name,current_ratio, quick_ratio, gross_profit_ratio, asset_turnover_ratio, debt_to_equity, pe, growth_rate)