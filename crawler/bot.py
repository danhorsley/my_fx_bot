import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
from sklearn.linear_model import LinearRegression

import datetime as dt     
start_date = dt.date.today()
y = dt.timedelta(days=1*365)
end_date = start_date + y
nb_paths = 10
initial_price = 1.10

def my_csv_reader(file, form = 'd'):
    """reads the csv file and converts the datetime into something useable"""
    eurusd = pd.read_csv('EURUSD_1d.csv')
    eurusd.columns= ['date','open','high','low','close','volume']
    eurusd['date'] = eurusd['date'].str.replace(r"GMT[+-]\d+", "")
    eurusd['date'] = pd.to_datetime(eurusd['date'],format='%d.%m.%Y %H:%M:%S.%f')#GMT')#+0100')
    eurusd = eurusd.set_index('date',drop=True)
    eurusd['returns'] = eurusd['close'].pct_change()
    return eurusd

def monte_carlo(frame, sd = start_date, ed = end_date, n = nb_paths,detrend=True):
    """Monte carlo simulation for date range - start date and end date
    n is number of simualations
    detrend will take trend out of data - i.e. absolute all values and assign + or - to returns
    with 50/50 probability"""
    dates = pd.bdate_range(sd, ed)
    nb_dates = len(dates)
    sample_source = frame['returns'].values[1:]
    if detrend:
        ss = pd.Series(sample_source).abs()
        ones = pd.Series([random.choice([-1,1]) for x in range(len(ss))])
        ss = ss * ones
        sampled_returns = np.random.choice(ss, size=(nb_dates-1, n))
    else:
        sampled_returns = np.random.choice(sample_source, size=(nb_dates-1, n))
    df_returns = pd.DataFrame(sampled_returns, index=dates[1:])
    df_price = (1 + df_returns).cumprod(axis=0)
    df_price.loc[dates[0], :] = 1.0
    df_price.sort_index(inplace=True)
    df_price *= initial_price
    return df_price

def plot_monte(mc, n = 15):
    return mc.iloc[:, 0:n].plot(figsize=(15,5))

def p_and_l(mc, t ):
    """generates position and p&l data"""
    col_name = mc.columns[0]
    frame = mc.copy()
    frame['trade'] = t
    frame['position'] = frame['trade'].cumsum()
    frame['position_value'] = frame[col_name] * frame['position']
    frame['cost'] = -frame[col_name]*frame['trade']
    frame['p_and_l'] = frame['position_value']+frame['cost'].cumsum()
    return frame

class trading_rules:
    """class to hold trading rules for bot"""
    def __init__(self,portfolio_size = 1000000 , trade_increment = 100000, 
                 stop_loss = -5, stop_profit = 10, 
                 trend_follow1=10, trend_follow2=30, trend_follow3=50,
                 mean_revert=False, trend_score = 0.8,):
        self.ps = portfolio_size
        self.ti = trade_increment
        self.sl = stop_loss
        self.sp = stop_profit
        self.tf1 = trend_follow1
        self.tf2 = trend_follow2
        self.tf3 = trend_follow3
        self.mr = mean_revert
        self.ts = trend_score
        self.rsl = 0   #rolling stop loss

    
    def trend_finder(self,rg):
        
        """rg is slice of the close prices"""
        col_name = rg.columns[0]
        slices = []
        for period in [self.tf1,self.tf2,self.tf3]: 
            if period != 0:
                slices.append(rg[-period:])

        lr = LinearRegression()
        correl = []
        coeff = []
        for sl in slices:
            X = np.array((sl.index -  sl.index[0]).days).reshape(-1,1)
            y = sl[col_name].values
            lr.fit(X,y)
            scr = lr.score(X,y)
            correl.append(scr)
            coeff.append(lr.coef_[0])
        #print(correl, coeff)
        return correl,coeff

    def trade_generator(self,test_monte_so_far,t_so_far):#,t_rules = trading_rules()):
        """generates trades given rules for bot"""
        frame = p_and_l(test_monte_so_far,t_so_far)
        new_trade = 0
        
        #finding trend conditions
        trend_scores = self.trend_finder(test_monte_so_far)#, s = t_rules.tf1, m = t_rules.tf2, l = t_rules.tf3)
        is_trend = np.where(pd.Series(trend_scores[0])>self.ts,1,0)  
        r2_condition = is_trend.sum()
        #print(r2_condition)
        coeff_dot = np.dot(np.array(trend_scores[1]), is_trend)
        direction = np.sign(np.dot(np.array(trend_scores[1]), is_trend)) 
        #stop loss or stop profit
        if frame['p_and_l'][-1] > self.ps * self.sp * 0.01 + self.rsl\
                                or frame['p_and_l'][-1] < self.ps * self.sl * 0.01 + self.rsl:
            new_trade = -frame['position'][-1]
            self.rsl = self.rsl + frame['p_and_l'][-1]

        #trend trades - check to see that you don't exceed portfolio size
        
        elif r2_condition == 1 and abs(frame['position'][-1] + direction*self.ti)<self.ps:
            #print('r2 check1')
            new_trade = np.sign(np.dot(np.array(trend_scores[1]), is_trend))*self.ti
            
        elif r2_condition >= 2 and abs(frame['position'][-1] + direction*self.ti)<self.ps:
            #print('r2 check1')
            
            if abs(frame['position'][-1] + 2*direction*self.ti) <= self.ps:
                new_trade = 2*direction*self.ti
            else:
                new_trade = direction*self.ti
        
            
        return new_trade

    def run_bot_over_montes(self, monte_group, pda = 50):#, tr = trading_rules()):
        """generates positions and p&ls for bot over different scenarios
        pda is the initial data before you start runnign the scenario"""
        trade_histories = []
        for j in tqdm(range(len(monte_group.columns))):
            self.rsl = 0
            monte = monte_group[[monte_group.columns[j]]]
            no_trades = [0 for x in range(pda)]
            for i in range(len(monte)-pda):
                new_trade = self.trade_generator(monte[:50+i],no_trades)#,t_rules =temp_tr)  #tr
                no_trades.append(new_trade)
            trade_history = p_and_l(monte,no_trades)
            trade_histories.append(trade_history)
        return trade_histories