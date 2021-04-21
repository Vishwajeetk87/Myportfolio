import yfinance as yf
import pandas as pd
from tickerdata.convert_df import sheets_to_df
from datetime import datetime
import cryptocompare
import sys


class Portfolio:

    def __init__(self):
        self.df_stocks = [self.cost_basis(dfr.get('frame'),dfr.get('tab')) for dfr in sheets_to_df()]
                              

    def _return(self, curr_price, cost_basis):
        val = float(curr_price)-float(cost_basis)

        return (float(val)/float(cost_basis))*100


    def cost_basis(self, dfr:list, tab):
        _df_stocks = dfr
        curr_price = 0
        for index, rows in _df_stocks.iterrows():
            
            if rows['Category'].lower() == 'stocks': 
                data = yf.download(tickers=rows['Ticker'], period='1d',interval='1m',progress=False)
                df_tail = data.tail(1)
                curr_price = "{:.2f}".format(df_tail.Close.values[0])
            elif rows['Category'].lower() == 'crypto':
                val = cryptocompare.get_price(rows['Ticker'], currency='USD')
                curr_price=val[rows['Ticker']]['USD'] 
            else:
                break
                
            _df_stocks.at[index,"Current_Price"] = curr_price
            _df_stocks.astype({"Current_Price":'float64'})
            _df_stocks.at[index,"Total_cost_basis"] = "{:.2f}".format(float(rows["Cost_Basis"]) * float(rows["Shares"]))
            _df_stocks.at[index,"Total_Value"] = "{:.2f}".format(float(curr_price) * float(rows["Shares"]))
            _df_stocks.at[index,"Return_%"] = "{:.2f}".format(self._return(curr_price, _df_stocks.iloc[index].Cost_Basis))
                
        _df_stocks=_df_stocks.astype({"Total_Value":'float64',"Return_%":'float64','Total_cost_basis':'float64'})
        return dict(frame=_df_stocks, tab=tab)

    def get_cash(self, df):
        cash_df = df[(df['Ticker']=='CASH')]
        return cash_df['Cost_Basis'] if len(cash_df)>0 else 0


    def portfolio_summary(self, port=None):

        total_net_profit = 0
        total_current_value = 0
        total_money_invested = 0
        total_cash = 0
        total_curr_np_cash = 0

        for df_stocks_iter in self.df_stocks:
            df_stocks=df_stocks_iter.get('frame')
           
            df_stocks=df_stocks[(df_stocks['Special']==port)] if port else df_stocks
            tab = df_stocks_iter.get('tab')
            if len(df_stocks):
                print_df = df_stocks.sort_values(by=['Return_%'], ascending=False)
                print(print_df)
                total_cb = df_stocks["Total_cost_basis"].sum()
                total_val = df_stocks["Total_Value"].sum()

                curr_net_profit = '{:.2f}'.format(total_val - total_cb)
                curr_gain_loss = '{:.2f}'.format((total_val - total_cb)/total_cb*100)
                curr_value = '{:.2f}'.format(total_val)
                curr_invest = '{:.2f}'.format(total_cb)
                cash = self.get_cash(df_stocks)
                
                curr_net_profit_cash = '{:.2f}'.format(total_val - float(cash)) if int(cash)>0 else 0
                curr_gain_loss_cash = '{:.2f}'.format(float(curr_net_profit_cash)/int(cash)*100) if int(cash)>0 else 0
                
                print(f"*******************")
                print(f"PORTFOLIO : {tab}")
                print(f"Net profit on Portfolio: {curr_net_profit}")
                print(f"Net profit on Cash Invested : {curr_net_profit_cash}")
                print(f"Gain/Loss on Portfolio : {curr_gain_loss}%")
                print(f"Gain loss on Cash Invested:{curr_gain_loss_cash}%")
                print(f"Current Value of {tab} :{curr_value}")
                print(f"Money Invested in {tab} :{curr_invest}")
                print("*******************")
            
                total_net_profit = float(curr_net_profit) + total_net_profit
                total_curr_np_cash = float(curr_net_profit_cash) + total_curr_np_cash
                total_cash = int(cash) + total_cash
                total_current_value = float(curr_value) + total_current_value
                total_money_invested = float(curr_invest) + total_money_invested

        if not port:
            print(f"##############################")
            print(f"TOTAL PORTFOLIO ")
            if total_cash>0:
                print(f"Total Net profit on Cash Invested: {'{:.2f}'.format(total_curr_np_cash)}")
                print(f"Total Gain/Loss on  Cash Invested: {'{:.2f}'.format(total_curr_np_cash/int(total_cash)*100)}%")
                print(f"Total cash invested : {'{:.2f}'.format(total_cash)}")
            else:
                sys.exit(f"Please enter cash deposited {tab} ")
            print(f"Total Portfolio Value  :{'{:.2f}'.format(total_current_value)}")
            print(f"Total Current Investment :{'{:.2f}'.format(total_money_invested)}")
            print("*******************")

