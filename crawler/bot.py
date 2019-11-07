#import pandas as pd
import numpy as np
import random
from tqdm import tqdm
#from sklearn.linear_model import LinearRegression
#from pandas.core.common import SettingWithCopyWarning
#import warnings
#from .dbtonumpy import eurusd_prices
#warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
from datetime import datetime, timedelta

import datetime as dt     
start_date = dt.date.today()
y = dt.timedelta(days=1*365)
end_date = start_date + y
nb_paths = 10
initial_price = 1.10


def r2_score_and_slope(y):
    """takes numpy array of prices and returns r2 score, slope and constant"""
    y = np.array(y)
    x = np.vstack([list(range(len(y))),np.ones(len(y))]).T
    m, c = np.linalg.lstsq(x, y, rcond=None)[0]
    y_hat = [(xx*m + c) for xx in list(range(len(y)))]
    y_bar = np.sum(y)/len(y)
    ssreg = np.sum((y_hat-y_bar)**2)   
    sstot = np.sum((y - y_bar)**2)
    r_2 = ssreg / sstot
    return r_2, m, c


import datetime as dt
def monte_carlo(arr, n_days=500, paths=100,detrend=True,starting_point = 1.1):
    """Monte carlo simulation for date range - start date and end date
    n is number of simualations
    detrend will take trend out of data - i.e. absolute all values and assign + or - to returns
    with 50/50 probability"""

    if detrend:
        ss = np.absolute(arr.reshape(1,-1))
        ones = np.random.choice([-1,1],len(arr))
        ss = ss * ones
        sampled_returns = np.random.choice(ss[0], size=(n_days, paths)) + 1
        #print(sampled_returns)
    else:
      sampled_returns = np.random.choice(array.reshape(1,-1)[0], size=(n_days, paths)) + 1
    date_list = [(datetime.today() + timedelta(days = i)) for i in range(n_days)]
    cum_returns = np.cumprod(sampled_returns,axis=0) * starting_point
    #df_price = pd.DataFrame(cum_returns, index = date_list)

    return [date_list,cum_returns]

def p_and_l_np(arr, all_trades):
  arr = np.array(arr)
  trades = np.array(all_trades)
  current_position = np.cumsum(trades)
  pos_value = arr * current_position
  cost = -arr*trades
  p_and_l = pos_value + np.cumsum(cost)
  return p_and_l, current_position

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def mean_reversion_np(arr,pda=50,devs=1,window=20):
  arr = np.array(arr)
  max_window = max(pda,window)
  std_rolling = np.std(rolling_window(arr, pda), 1)
  mov_av = np.mean(rolling_window(arr, window), 1)
  devs_away = np.where(abs(mov_av[max(0,pda-window):]-arr[max_window-1:])>=std_rolling[max(0,window-pda):]*devs,1,0)
  b_or_s = np.where(mov_av[max(0,pda-window):]-arr[max_window-1:]>=0,1,-1)
  action = b_or_s * devs_away
  action_shift = action[1:]
  mr_trade = np.append(action[0], action_shift - action[:-1])
  #return np.append(np.zeros(pda-1),mr_trade)
  return mr_trade



class trading_rules:
    """class to hold trading rules for bot"""
    def __init__(self,portfolio_size = 1000000 , trade_increment = 100000, 
                 stop_loss = -5, stop_profit = 10, 
                 trend_follow1=10, trend_follow2=30, trend_follow3=50,
                 mean_revert=False, mean_revert_inc = 0.5, trend_score = 0.8,):
        self.ps = portfolio_size
        self.ti = trade_increment
        self.sl = stop_loss
        self.sp = stop_profit
        self.tf1 = trend_follow1
        self.tf2 = trend_follow2
        self.tf3 = trend_follow3
        self.mr = mean_revert
        self.mr = mean_revert
        self.mri =  mean_revert_inc
        self.ts = trend_score
        self.rsl = 0   #rolling stop loss

    
    def trend_finder(self,rg):
        
        """rg is slice of the close prices"""
        #col_name = rg.columns[0]
        slices = []
        for period in [self.tf1,self.tf2,self.tf3]: 
            if period != 0:
                slices.append(rg[-period:])
        correl = []
        coeff = []
        for sl in slices:
            y = np.array(sl)
            scr, m, c = r2_score_and_slope(y)
            correl.append(scr)
            coeff.append(m)
        #print(correl, coeff)
        return correl,coeff

    def trade_generator(self,test_monte_so_far,t_so_far):#,t_rules = trading_rules()):
        """generates trades given rules for bot"""
        #frame = p_and_l(test_monte_so_far,t_so_far)
        p_and_l, cur_pos = p_and_l_np(test_monte_so_far,t_so_far)
        new_trade = 0
        
        #finding trend conditions
        trend_scores = self.trend_finder(test_monte_so_far)#, s = t_rules.tf1, m = t_rules.tf2, l = t_rules.tf3)
        is_trend = np.where(np.array(trend_scores[0])>self.ts,1,0)  
        r2_condition = is_trend.sum()
        #print(r2_condition)
        coeff_dot = np.dot(np.array(trend_scores[1]), is_trend)
        direction = np.sign(np.dot(np.array(trend_scores[1]), is_trend)) 
        #stop loss or stop profit
        if p_and_l[-1] > self.ps * self.sp * 0.01 + self.rsl\
                                or p_and_l[-1] < self.ps * self.sl * 0.01 + self.rsl:
            new_trade = -cur_pos[-1]
            self.rsl = self.rsl + p_and_l[-1]

        #trend trades - check to see that you don't exceed portfolio size
        
        elif r2_condition == 1 and abs(cur_pos[-1] + direction*self.ti)<self.ps:

            new_trade = np.sign(np.dot(np.array(trend_scores[1]), is_trend))*self.ti
            
        elif r2_condition >= 2 and abs(cur_pos[-1] + direction*self.ti)<self.ps:
            
            if abs(cur_pos[-1] + 2*direction*self.ti) <= self.ps:
                new_trade = 2*direction*self.ti
            else:
                new_trade = direction*self.ti
            
        return new_trade

    def run_bot_over_montes(self, monte_group, pda = 50):#, tr = trading_rules()):
        """generates positions and p&ls for bot over different scenarios
        pda is the initial data before you start runnign the scenario"""
        trade_histories = []
        for j in tqdm(range(len(monte_group[1][0]))):
            self.rsl = 0
            #monte = monte_group[[monte_group.columns[j]]].copy()
            monte = monte_group[1][:,j]
            #print(monte.shape)
            #monte = make_reversion_columns(monte)
            mr_trade = mean_reversion_np(monte,pda=pda) * self.mri*self.ps
            no_trades = [0 for x in range(pda)]
            for i in range(len(monte)-pda):
                new_trade = self.trade_generator(monte[:pda+i],no_trades)
                #adding mean reversion here to try and speed up
                #mr_trade = monte['mr_trade'][pda+i] * self.mri*self.ps
                new_trade = new_trade + mr_trade[i]
                no_trades.append(new_trade)
            trade_history = p_and_l_np(monte,no_trades)
            trade_histories.append(trade_history)
        return trade_histories