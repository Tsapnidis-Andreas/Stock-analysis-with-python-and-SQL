# Project Title
## Stock Analysis with Python/SQL <br>
# Contents
[Info](#Info)<br>
[Fundamental Analysis](#Fundamental-Analysis)<br>
[Market Performance Analysis](#Market-Performance-Analysis)<br>
[Disclaimer](#Disclaimer)
# Info
## Programming Languages: 
Python <br>
SQL <br>
## Libraries used:
[Pandas](https://pandas.pydata.org/#:~:text=pandas%20is%20a%20fast,%20powerful,%20flexible)<br>
[Numpy](https://numpy.org/)<br>
[Matplotlib](https://matplotlib.org/)<br>
[Yfinance](https://pypi.org/project/yfinance/)<br>
[Datetime](https://docs.python.org/3/library/datetime.html)<br>
[Pyodbc](https://pypi.org/project/pyodbc/)<br>
[Scipy](https://scipy.org/)<br>
# Fundamental Analysis
## How to use
Create a Database accessible with SQL code<br>
Create a table as described in the file 'SQl commands.txt'<br>
Install the Python libraries mentioned above<br>
Initialize the variable ‘stock_name’ with the ticker symbol of the company<br>
Initialize the variable ‘path’ with the directory where the .xlsx file will be saved<br>
Run the code<br>



## How it works
### The code entails:
The code entails
Downloading the company’s balance sheet and income statement via the library yfinance<br>
Using data pulled from  the financial statements to calculate the following:<br>
current ratio /quick ratio /gross profit margin/ asset turnover ratio/debt to equity<br>
P/E ratio/growth rate<br>
Saving all the relevant data in an .xlsx file<br>
Storing the data in the database where they are easily accessible with SQL commands for<br> further analysis<br>
## Example
![Screenshot of the Table](https://github.com/user-attachments/assets/5d2e6774-20e3-4224-a120-f0170f6ffe07)



# Market Performance Analysis

## How to use
Create a Database accessible with SQL code<br>
Create a table as described here<br>
Install the Python libraries mentioned above<br>
Initialize the variable ‘stock_name’ with the ticker symbol of the company<br>
Initialize the variable ‘path’ with the directory where the .xlsx file will be saved<br>
Run the code<br>


## How it works
The code entails:<br>
Pulling market data using the yfinance library<br>
Calculating the average monthly return and standard deviation of the stock<br>
Calculating the beta coefficient of the stock<br>
Calculating the sharpe and treynor ratios<br>
Saving all the relevant data in an .xlsx file<br>
Creating various graphs<br>





## Example
![Στιγμιότυπο οθόνης 2024-09-17 175448](https://github.com/user-attachments/assets/d6a7f0aa-8bd3-4711-866e-ddce3be3eb6a)
![Στιγμιότυπο οθόνης 2024-09-17 175505](https://github.com/user-attachments/assets/ce37ec5a-375a-4522-a0eb-0e939099bd1e)


# Disclaimer
This project serves educational purposes only<br>
Under no circumstances should it be used as an investing tool
