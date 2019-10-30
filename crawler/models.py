from flask_sqlalchemy import SQLAlchemy
from .__init__ import DB
import time as time

class Leaderboard(DB.Model):
    """Twitter users that we pull and analyse tweets for"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    ltsm = DB.Column(DB.Boolean, nullable = False)
    trend = DB.Column(DB.Integer, nullable = False)
    stop_loss = DB.Column(DB.Integer, nullable = False)
    stop_proft = DB.Column(DB.Integer, nullable = False)
    profit = DB.Column(DB.BigInteger, nullable=False)
    sim_number = DB.Column(DB.Integer, nullable = False)
    currency = DB.Column(DB.Text, nullable = False)

  
    def __init__(self, id, ltsm, trend, stop_loss, stop_profit, profit, sim_number, currency):
        self.id=time()
        self.ltsm = ltsm
        self.trend = trend
        self.stop_loss = stop_loss
        self.stop_profit = stop_profit
        self.sim_number = sim_number
        self.currency = currency
    
    def __repr__(self):
         return '<id {}, ltsm {}, trend {}, stop_l {},stop_p {},  profit{}, sims {} ccy {}>'.format(self.id,
                                                                                            self.ltsm,
                                                                                            self.trend,
                                                                                            self.stop_l,
                                                                                            self.stop_p,
                                                                                            self.profit,
                                                                                            self.sims,
                                                                                            self.ccy)