from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['ENV'] = 'debug'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """render base.html"""

    return render_template('base.html')

@APP.route('/', methods=['POST'])
def my_form_post():
    ts = request.form['time_series']
    sn = request.form['sim_number']
    processed_text = ts.lower() + str(sn)
    return processed_text

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

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    price = DB.Column(DB.Float, nullable=False)
    #lat = DB.Column(DB.Float)
    #lon = DB.Column(DB.Float)


    def __repr__(self):
        return '<Date :{}> <Price :{}>'.format(self.datetime,self.price)