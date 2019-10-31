from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
#import matplotlib.pyplot as plt
from .bot import *
import os
import pygal
from pygal.style import Style
from .__init__ import APP, DB
from .models import Leaderboard
from time import time

@APP.route('/')
def root():
    """render base.html"""

    return render_template('base.html')

@APP.route('/', methods=['POST'])
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
    
    my_label = f'{ts}_1d.csv'  #read the time series csv - #TODO change this to Model in Heroku
    df = my_csv_reader(my_label, form = 'd')

    mc = monte_carlo(df, sd = start_date, ed = end_date, n = sn, detrend = True)

    #creating trades for simulations
    my_trading_rules = trading_rules(portfolio_size = 1000000 , trade_increment = 100000,
                                        stop_loss = sl, stop_profit = sp, 
                                        trend_follow1 = tf1, trend_follow2 = tf2,trend_follow3 = tf3,
                                        mean_revert = mr,  mean_revert_inc = 1, trend_score = 0.8)
    scenarios = my_trading_rules.run_bot_over_montes(mc, pda = 50)#, tr = my_trading_rules)
    results = []
    for scenario in scenarios:
        _ = scenario['p_and_l'][-1]
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
    line_chart.x_labels = ({
                        'label': f'{start_date}',
                        'value': start_date
                        }, {
                        'label': f'{end_date}',
                        'value': end_date})
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
        line_chart.add(f'simulation {n + 1}',  mc[n], show_only_major_dots=True)
        bar_chart.add(f'simulation {n + 1}', my_dict[n+1])
    avg_profit = int(sum(my_dict.values())/len(my_dict))
    bar_chart.add(f'average', avg_profit)
    pyg_chart = line_chart.render_data_uri()
    pyg_bar = bar_chart.render_data_uri()

    scenario_zero = scenarios[0]
    leaderboard_entry = Leaderboard(id = time(),ltsm = ltsm, trend1 = tf1, trend2 = tf2, trend3 = tf3,
                                     mr = mr, stop_loss = sl, stop_profit = sp, profit = avg_profit,
                                     sim_number = sn, currency = ts, )

    
    DB.session.add(leaderboard_entry)
    DB.session.commit()

    return render_template('plot_render.html', name = 'Simulation Results',
    #  url ='static/images/new_plot2.png',
     tables = [scenario_zero.to_html(classes='data')], 
     titles = scenario_zero.columns.values,
     results = results,
     scenario_z = scenario_zero,
     pyg = pyg_chart,
     pyg_b = pyg_bar)


@APP.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@APP.route('/db_reset')
def dbr():
    """fully reset models"""
    DB.drop_all()
    DB.create_all()

    return 'db reset'

@APP.route('/leaderboard')
def leader():
    """fully reset models"""
    my_query = DB.session.query().all()

    return my_query
    
