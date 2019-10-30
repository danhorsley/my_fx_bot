from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
from .bot import *
import os
import pygal
from pygal.style import Style
from .__init__ import APP, DB

# APP = Flask(__name__)
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# #APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# APP.config['ENV'] = 'debug'
# DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """render base.html"""

    return render_template('base.html')

@APP.route('/', methods=['POST'])
def my_form_post():
    ts = request.form['time_series']
    sn = int(request.form['sim_number'])
    my_label = f'{ts}_1d.csv'
    df = my_csv_reader(my_label, form = 'd')
    mc = monte_carlo(df, sd = start_date, ed = end_date, n = sn, detrend = True)
    
    #creating plot of simulations
    # plt.clf()
    # plt.plot(mc.iloc[:, :10])
    # strFile = 'crawler/static/images/new_plot2.png'
    # if os.path.isfile(strFile):
    #     os.remove(strFile)
    # plt.savefig(strFile)

    #creating trades for simulations
    scenarios = run_bot_over_montes(mc, pda = 50, tr = trading_rules())
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
        legend_font_size=20,
        title_font_size=30,
        font_family = 'googlefont:Inconsolata')

    line_chart = pygal.Line(width=1000,height=500, style = custom_style)  #width=1500,height=500, 
    bar_chart = pygal.Bar(width=750, style = custom_style)  #width=500,height=250, Horizontal
    #bar_chart = pygal.Bar(style = custom_style)

    line_chart.title = f'{sn} Monte Carlo EURUSD simulations'
    bar_chart.title = 'profit and loss by simulation'
    #bar_chart.add('p&l by simulation',my_dict.values())
    line_chart.x_labels = map(str, mc[0].index)
    #bar_chart.x_labels = map(str, my_dict.keys()) #range(2002, 2013))
    for n in range(sn):
        line_chart.add(f'simulation {n}',  mc[n], show_only_major_dots=True)
        bar_chart.add(f'simulation {n}', my_dict[n+1])
        # [{'value' : my_dict[n+1], 'color' :f'rgba({(my_dict[n+1]/max(my_dict.values()))}, 45,20,0.6)'}])
        #bar_chart.add(f'simualation {n}', my_dict[n])

    pyg_chart = line_chart.render_data_uri()
    pyg_bar = bar_chart.render_data_uri()

    

    return render_template('plot_render.html', name = 'Simulation Results',
    #  url ='static/images/new_plot2.png',
    #  url2 ='static/images/bar_plot.png',
     tables = [scenario_zero.to_html(classes='data')], 
     titles = scenario_zero.columns.values,
     average_panl = result_avg, worst_panl = result_worst, best_panl = results_best, results = results,
     scenario_z = scenario_zero,
     pyg = pyg_chart,
     pyg_b = pyg_bar)
    #this returns rendered times series
    #return render_template('dataframe.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

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

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    return render_template('base.html')

@APP.route('/my_form')#, methods=['POST'])
def my_form():
    #form_input = request.form['ts_content']
    #print(form_input)
    # Now that get value back to server can send it to a DB(use Flask-SQLAlchemy)
    return "submitted"

@APP.route('/pygal')
def pyg():
    """render base.html"""
    N = 5
    my_label = 'EURUSD_1d.csv'
    df = my_csv_reader(my_label, form = 'd')
    mc = monte_carlo(df, sd = start_date, ed = end_date, n = 5, detrend = True)
    line_chart = pygal.Line(width=1500,height=500)
    line_chart.title = f'{N} Monte Carlo EURUSD simulations'
    line_chart.x_labels = map(str, mc[0].index) #range(2002, 2013))
    for n in range(N):
        line_chart.add(f'simulation {n}',  mc[n], show_only_major_dots=True)

    line_chart.render()

    return line_chart.render_response()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    price = DB.Column(DB.Float, nullable=False)
    #lat = DB.Column(DB.Float)
    #lon = DB.Column(DB.Float)


    def __repr__(self):
        return '<Date :{}> <Price :{}>'.format(self.datetime,self.price)