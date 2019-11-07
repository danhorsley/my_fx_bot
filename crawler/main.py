from flask import Flask, render_template, request, Response, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from .bot import *
import os
import pygal
from pygal.style import Style
from . import  DB  #APP,
from .models import *#Leaderboard #, EURUSD, model_dict
DB.create_all()
DB.session.commit()
from .dbtonumpy import *
from time import time
import json

main = Blueprint('main', __name__)  #changed @APPs to @main and / to home

@main.route('/')
def index():
    return 'Index'

@main.route('/profile')
def profile():
    return 'Profile'

@main.route('/home')
@login_required
def home():
    """render home screen"""

    return render_template('home.html', name = current_user.name)

@main.route('/home', methods=['POST'])
@login_required
def my_form_post():
    ts = request.form['time_series']  #which currency
    sn = int(request.form['sim_number']) #number of mc sims to run
    tf1 = int(request.form['tf1'])  #trend to follow 1
    tf2 = int(request.form['tf2'])  #trend to follow 2
    tf3 = int(request.form['tf3'])  #trend to follow 3
    ltsm = int(request.form['ltsm'])  #trend to follow
    sl = int(request.form['sl'])  #stop loss
    sp = int(request.form['sp'])  #stop profit
    mr = int(request.form['mr'])   #mean reversion
    
    #my_label = f'{ts}_1d.csv'  #read the time series csv - #TODO change this to Model in Heroku
    my_label = ts
    #df = my_csv_reader(my_label, form = 'd')
    eurusd_prices = np.array(DB.session.query(EURUSD.price).order_by(asc(EURUSD.date)).all(),
                                         dtype='float')

    price_dict = {'EURUSD':eurusd_prices}
    my_arr = price_dict[my_label]
    returns = np.diff(my_arr,axis=0)/my_arr[:-1]
    #mc = monte_carlo(df, sd = start_date, ed = end_date, n = sn, detrend = True)
    mc = monte_carlo(returns,n_days=500, paths=sn,detrend=True,starting_point = 1.1)
    #creating trades for simulations
    my_trading_rules = trading_rules(portfolio_size = 1000000 , trade_increment = 100000,
                                        stop_loss = sl, stop_profit = sp, 
                                        trend_follow1 = tf1, trend_follow2 = tf2,trend_follow3 = tf3,
                                        mean_revert = mr,  mean_revert_inc = 1, trend_score = 0.8)
    scenarios = my_trading_rules.run_bot_over_montes(mc, pda = 50)#, tr = my_trading_rules)
    results = []
    for scenario in scenarios:
        _ = scenario[0][-1]
        results.append(_)
    
    my_dict = {}
    for n,l in enumerate(results):
        my_dict[n+1]=int(l)  #change results to int

    custom_style = Style(
        label_font_size=20,
        major_label_font_size = 20,
        legend_font_size=20,
        title_font_size=30,
        font_family = 'googlefont:Inconsolata')

    line_chart = pygal.Line(width=1000,height=500, style = custom_style, show_dots=False)   
    bar_chart = pygal.Bar(width=1150, style = custom_style) 

    line_chart.title = f'{sn} Monte Carlo {ts} simulations'
    bar_chart.title = 'profit and loss by simulation'
    # line_chart.x_labels = ({
    #                     'label': f'{datetime.today()}',
    #                     'value': datetime.today()
    #                     }, {
    #                     'label': f'{datetime.today()+dt.timedelta(days=1*500)}',
    #                     'value': datetime.today()+dt.timedelta(days=1*500)})
    bar_chart.y_labels = ({
                        'label': '-150k',
                        'value': -150000
                        }, {
                        'label': '-75k',
                        'value': -75000
                        }, {
                        'label': '0k',
                        'value': 0
                        }, {
                        'label': '75k',
                        'value': 75000
                        }, {
                        'label': '150k',
                        'value': 150000})
    for n in range(sn):
        #print(mc[1][:,n])
        line_chart.add(f'simulation {n + 1}',  mc[1][:,n], show_only_major_dots=True)  #change here 
        bar_chart.add(f'simulation {n + 1}', my_dict[n+1])
    avg_profit = int(sum(my_dict.values())/len(my_dict))
    bar_chart.add(f'average', avg_profit)
    pyg_chart = line_chart.render_data_uri()
    pyg_bar = bar_chart.render_data_uri()

    #scenario_zero = scenarios[0]
    leaderboard_entry = Leaderboard(id = time(),name = current_user.name,ltsm = ltsm, 
                                    trend1 = tf1, trend2 = tf2, trend3 = tf3,
                                     mr = mr, stop_loss = sl, stop_profit = sp, profit = avg_profit,
                                     sim_number = sn, currency = ts, )

    
    DB.session.add(leaderboard_entry)
    DB.session.commit()

    return render_template('plot_render.html', name = 'Simulation Results',
    #  url ='static/images/new_plot2.png',
     #tables = [scenario_zero.to_html(classes='data')], 
     #titles = scenario_zero.columns.values,
     results = results,
     #scenario_z = scenario_zero,
     pyg = pyg_chart,
     pyg_b = pyg_bar)



@main.route('/db_reset')
#@login_required
def dbr():
    """fully reset models"""
    DB.drop_all()
    DB.create_all()

    return 'db reset'

@main.route('/pop_ccy')
def pop_form():
    return render_template('pop_ccy.html')


@main.route('/pop_ccy', methods=['POST'])
#@login_required
def pop():
    """populate historical currencirs"""
    from forex_python.converter import CurrencyRates
    from datetime import datetime, timedelta
    from sqlalchemy.sql import func

    ccy1 = request.form['ccy1']
    ccy2 = request.form['ccy2']
    ccy_pair = ccy1 + ccy2
    pop_start = datetime.strptime(request.form['pop_start'],'%Y-%m-%d')
    pop_end = datetime.strptime(request.form['pop_end'],'%Y-%m-%d')
    mind = DB.session.query(func.min(model_dict[ccy_pair].date)).all()[0][0]
    maxd = DB.session.query(func.max(model_dict[ccy_pair].date)).all()[0][0]
    if mind is not None:
        min_date = datetime.strptime(mind,'%Y-%m-%d  00:00:00')
    else:
        min_date = datetime.min
    if maxd is not None:
        max_date = datetime.strptime(maxd,'%Y-%m-%d  00:00:00')
    else:
        max_date = datetime.min
    print('currencies',ccy1,ccy2)
    print(pop_end,pop_start,min_date,max_date)
    if pop_end <= min_date or pop_start >= max_date:
        delta = pop_end - pop_start
        date_list = [(pop_start + timedelta(days = i)) for i in range(delta.days+1)]
    elif pop_start < min_date and pop_end <= max_date:
        delta = min_date - pop_start - timedelta(days=1)
        date_list = [(pop_start + timedelta(days = i)) for i in range(delta.days+1)]
    elif pop_start >= min_date and pop_end <=max_date:
        delta = 0
        date_list = []
    elif pop_start < min_date and pop_end > max_date:
        delta = min_date - pop_start - timedelta(days=1)
        delta2 = pop_end - max_date - timedelta(days=1)
        date_list = [(pop_start + timedelta(days = i)) for i in range(delta.days+1)]
        date_list = date_list + [(max_date + timedelta(days = i)) for i in range(1,delta2.days+1)]
    elif pop_start >= min_date and pop_end > max_date:
        delta = pop_end - max_date  - timedelta(days=1)
        date_list =[(max_date + timedelta(days = i)) for i in range(1,delta.days+1)]
    #delta = pop_end - pop_start
    #date_list = [(pop_start + timedelta(days = i)) for i in range(delta.days+1)]

    c = CurrencyRates()
    print(date_list)
    for dat in date_list:
        print('datecheck',dat)
        # if DB.session.query(model_dict[ccy_pair]).filter(model_dict[ccy_pair].date==dat).count() > 0:
        #     pass
        # else:
        _ = c.get_rate(ccy1, ccy2, dat)
        ccy = model_dict[ccy_pair](date = dat, price = _)
        DB.session.add(ccy)
    DB.session.commit()  

    return 'ccy popped'

@main.route('/leaderboard')
@login_required
def leader():
    """fully reset models"""
    my_query = DB.session.query(Leaderboard.profit,Leaderboard.name, Leaderboard.sim_number,Leaderboard.mr,
                                    Leaderboard.trend1,Leaderboard.trend2,Leaderboard.trend3, 
                                    Leaderboard.stop_loss, Leaderboard.stop_profit,Leaderboard.currency,
                                     Leaderboard.ltsm).order_by(Leaderboard.profit.desc()).all()
    my_query = pd.DataFrame(my_query)
    #print(my_query.head())
    my_query.columns= ['average profit','name','number of sims','mean reversion','trend1','trend2','trend3',
                        'stop_loss','stop_profit','currency','ltsm']
    return render_template('leaderboard.html', name = 'Leaderboard', 
                                ldr = [my_query.to_html(classes='data')],
                                 titles = my_query.columns.values)
    
