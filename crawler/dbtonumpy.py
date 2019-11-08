import numpy as np
from .models import EURUSD, USDJPY, EURJPY, GBPUSD, GBPJPY 
from . import DB
from sqlalchemy import asc


def create_price(currency):

    if currency =='EURUSD':
        eurusd_prices = np.array(DB.session.query(EURUSD.price).order_by(asc(EURUSD.date)).all(),
                                            dtype='float')
        return eurusd_prices
    elif currency =='USDJPY':
        usdjpy_prices = np.array(DB.session.query(USDJPY.price).order_by(asc(USDJPY.date)).all(),
                                            dtype='float')
        return usdjpy_prices
    elif currency =='EURJPY':
        eurjpy_prices = np.array(DB.session.query(EURJPY.price).order_by(asc(EURJPY.date)).all(),
                                            dtype='float')
        return eurjpy_prices
    elif currency =='GBPUSD':
        gbpusd_prices = np.array(DB.session.query(GBPUSD.price).order_by(asc(GBPUSD.date)).all(),
                                            dtype='float') 
        return gbpusd_prices     
    elif currency =='GBPJPY':
        gbpjpy_prices = np.array(DB.session.query(GBPJPY.price).order_by(asc(GBPJPY.date)).all(),
                                            dtype='float')  
        return gbpjpy_prices                                 



    # price_dict = {'EURUSD':eurusd_prices, 'USDJPY':usdjpy_prices, 
    #                 'EURJPY':eurjpy_prices, 'GBPUSD':gbpusd_prices,
    #                 'GBPJPY':gbpjpy_prices}

    # last_price_dict = {'EURUSD':eurusd_prices[-1], 'USDJPY':usdjpy_prices[-1], 
    #                 'EURJPY':eurjpy_prices[-1], 'GBPUSD':gbpusd_prices[-1],
    #                 'GBPJPY':gbpjpy_prices[-1]}

    # return price_dict(currency), last_price_dict(currency)