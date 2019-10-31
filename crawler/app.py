from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
#import matplotlib.pyplot as plt
from .bot import *
import os
import pygal
from pygal.style import Style
from .__init__ import APP, DB

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
    
    my_label = f'{ts}_1d.csv'  #read the time series csv - #TODO change this to Model in Heroku
    df = my_csv_reader(my_label, form = 'd')

    mc = monte_carlo(df, sd = start_date, ed = end_date, n = sn, detrend = True)

    #creating trades for simulations
    my_trading_rules = trading_rules(portfolio_size = 1000000 , trade_increment = 100000,
                                        stop_loss = sl, stop_profit = sp, 
                                        trend_follow1 = tf1, trend_follow2 = tf2,trend_follow3 = tf3,
                                        mean_revert = False, trend_score = 0.8)
    scenarios = my_trading_rules.run_bot_over_montes(mc, pda = 50)#, tr = my_trading_rules)
    results = []
    for scenario in scenarios:
        _ = scenario['p_and_l'][-1]
        results.append(_)
    
    my_dict = {}
    for n,l in enumerate(results):
        my_dict[n+1]=l
    
    result_avg = sum(results)/len(results)
    result_worst = min(results)
    results_best = max(results)
    scenario_zero = scenarios[0]

    # plt.clf()
    # data_color = [x / max(results) for x in results]
    # my_cmap = plt.cm.get_cmap('RdBu')
    # colors = my_cmap(data_color)
    # plt.bar(x=my_dict.keys(),height = my_dict.values(),width=0.8,color=colors)
    # strFile2 = 'crawler/static/images/bar_plot.png'
    # if os.path.isfile(strFile2):
    #     os.remove(strFile2)
    # plt.savefig(strFile2)
    #default font is Inconsolata
    custom_style = Style(
        label_font_size=20,
        major_label_font_size = 20,
        legend_font_size=20,
        title_font_size=30,
        font_family = 'googlefont:Inconsolata')

    line_chart = pygal.Line(width=1000,height=500, style = custom_style, show_dots=False)  #width=1500,height=500, 
    bar_chart = pygal.Bar(width=1150, style = custom_style)  #width=500,height=250, Horizontal
    #bar_chart = pygal.Bar(style = custom_style)

    line_chart.title = f'{sn} Monte Carlo {ts} simulations'
    bar_chart.title = 'profit and loss by simulation'
    #bar_chart.add('p&l by simulation',my_dict.values())
    #line_chart.x_labels = map(str, mc[0].index)
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
    #bar_chart.x_labels = map(str, my_dict.keys()) #range(2002, 2013))
    for n in range(sn):
        line_chart.add(f'simulation {n + 1}',  mc[n], show_only_major_dots=True)
        bar_chart.add(f'simulation {n + 1}', my_dict[n+1])
        # [{'value' : my_dict[n+1], 'color' :f'rgba({(my_dict[n+1]/max(my_dict.values()))}, 45,20,0.6)'}])
        #bar_chart.add(f'simualation {n}', my_dict[n])
    bar_chart.add(f'average', sum(my_dict.values())/len(my_dict))
    pyg_chart = line_chart.render_data_uri()
    pyg_bar = bar_chart.render_data_uri()

    

    return render_template('plot_render.html', name = 'Simulation Results',
    #  url ='static/images/new_plot2.png',
     tables = [scenario_zero.to_html(classes='data')], 
     titles = scenario_zero.columns.values,
     average_panl = result_avg, worst_panl = result_worst, best_panl = results_best, results = results,
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

    return 'DB reset'
    
