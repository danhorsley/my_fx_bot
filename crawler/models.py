from flask_sqlalchemy import SQLAlchemy
from . import DB
from time import time

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = DB.Column(DB.String(100), unique=True)
    password = DB.Column(DB.String(100))
    name = DB.Column(DB.String(1000))

class Leaderboard(DB.Model):
    """Twitter users that we pull and analyse tweets for"""
    id = DB.Column(DB.Float, primary_key=True)
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

  
    def __init__(self, id, ltsm, trend1, trend2, trend3, mr, stop_loss, stop_profit, profit, sim_number, currency):
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
         return '<id {}, ltsm {}, trend {}, stop_l {},stop_p {},  profit{}, sims {} ccy {}>'.format(self.id,
                                                                                            self.ltsm,
                                                                                            self.trend,
                                                                                            self.stop_loss,
                                                                                            self.stop_profit,
                                                                                            self.profit,
                                                                                            self.sims,
                                                                                            self.ccy)