import numpy as np
from .models import EURUSD, USDJPY, EURJPY, GBPUSD, GBPJPY 
from . import DB
from sqlalchemy import asc

# eurusd_array = np.array(DB.session.query(EURUSD.date,EURUSD.price).all(),
#                                     dtype=[('date', 'datetime64[D]'),('price', 'float')])

eurusd_prices = np.array(DB.session.query(EURUSD.price).order_by(asc(EURUSD.date)).all(),
                                    dtype='float')

usdjpy_prices = np.array(DB.session.query(USDJPY.price).order_by(asc(USDJPY.date)).all(),
                                    dtype='float')

eurjpy_prices = np.array(DB.session.query(EURJPY.price).order_by(asc(EURJPY.date)).all(),
                                    dtype='float')

gbpusd_prices = np.array(DB.session.query(GBPUSD.price).order_by(asc(GBPUSD.date)).all(),
                                    dtype='float')      

gbpjpy_prices = np.array(DB.session.query(GBPJPY.price).order_by(asc(GBPJPY.date)).all(),
                                    dtype='float')                                   



price_dict = {'EURUSD':eurusd_prices, 'USDJPY':usdjpy_prices, 
                'EURJPY':eurjpy_prices, 'GBPUSD':gbpusd_prices,
                'GBPJPY':gbpjpy_prices}