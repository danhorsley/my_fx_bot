from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import DB
from time import time
#from SQLAlchemy.types import TypeDecorator
import json


class User(DB.Model, UserMixin):
    id = DB.Column(DB.Integer, primary_key=True, unique=True) # primary keys are required by SQLAlchemy
    email = DB.Column(DB.String(100), unique=True)
    password = DB.Column(DB.String(100))
    name = DB.Column(DB.String(100), unique=True)

class EURUSD(DB.Model):#(Historical):
    #__bind_key__ = "EURUSD"
    date = DB.Column(DB.String(100), primary_key=True)
    price = DB.Column(DB.Float, nullable = False)

class GBPUSD(DB.Model):#(Historical):
    #__bind_key__ = "EURUSD"
    date = DB.Column(DB.String(100), primary_key=True)
    price = DB.Column(DB.Float, nullable = False)

class GBPJPY(DB.Model):#(Historical):
    #__bind_key__ = "EURUSD"
    date = DB.Column(DB.String(100), primary_key=True)
    price = DB.Column(DB.Float, nullable = False)

class USDJPY(DB.Model):#(Historical):
    #__bind_key__ = "EURUSD"
    date = DB.Column(DB.String(100), primary_key=True)
    price = DB.Column(DB.Float, nullable = False)

class EURJPY(DB.Model):#(Historical):
    #__bind_key__ = "EURUSD"
    date = DB.Column(DB.String(100), primary_key=True)
    price = DB.Column(DB.Float, nullable = False)

model_dict = {"EURUSD" : EURUSD, "GBPUSD" : GBPUSD, "GBPJPY" : GBPJPY,"USDJPY" : USDJPY, "EURJPY" : EURJPY}

class Leaderboard(DB.Model):
    """Leaderboard model storing best of the sims"""
    id = DB.Column(DB.Float, primary_key=True)
    name = DB.Column(DB.String(100),DB.ForeignKey('user.name'),nullable=False)
    ltsm = DB.Column(DB.Boolean, nullable = False)
    mr = DB.Column(DB.Boolean, nullable = False)
    trend1 = DB.Column(DB.Integer, nullable = False)
    trend2 = DB.Column(DB.Integer, nullable = False)
    trend3 = DB.Column(DB.Integer, nullable = False)
    stop_loss = DB.Column(DB.Integer, nullable = False)
    stop_profit = DB.Column(DB.Integer, nullable = False)
    profit = DB.Column(DB.BigInteger, nullable=False)
    sim_number = DB.Column(DB.Integer, nullable = False)
    currency = DB.Column(DB.Text, nullable = False)

  
    def __init__(self, id, name, ltsm, trend1, trend2, trend3, mr, stop_loss, stop_profit, profit, sim_number, currency):
        self.name = name
        self.id=time()
        self.ltsm = ltsm
        self.trend1 = trend1
        self.trend2 = trend2
        self.trend3 = trend3
        self.mr = mr
        self.stop_loss = stop_loss
        self.stop_profit = stop_profit
        self.profit = profit
        self.sim_number = sim_number
        self.currency = currency
    
    def __repr__(self):
         return '<id {}, ltsm {}, trend1 {}, trend2 {},trend3 {},stop_l {},stop_p {},  profit{}, sims {} ccy {}>'.format(self.id,
                                                                                            self.ltsm,
                                                                                            self.trend1,
                                                                                            self.trend2,
                                                                                            self.trend3,
                                                                                            self.stop_loss,
                                                                                            self.stop_profit,
                                                                                            self.profit,
                                                                                            self.sim_number,
                                                                                            self.currency)