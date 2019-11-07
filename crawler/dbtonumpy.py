import numpy as np
#from .models import EURUSD
from . import DB
from sqlalchemy import asc

# eurusd_array = np.array(DB.session.query(EURUSD.date,EURUSD.price).all(),
#                                     dtype=[('date', 'datetime64[D]'),('price', 'float')])

# eurusd_prices = np.array(DB.session.query(EURUSD.price).order_by(asc(EURUSD.date)).all(),
#                                     dtype='float')

# price_dict = {'EURUSD':eurusd_prices}