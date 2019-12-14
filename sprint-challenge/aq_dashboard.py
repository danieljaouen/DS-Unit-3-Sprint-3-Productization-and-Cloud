import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'Record < Value {self.value} --- Time {self.datetime}>'


def get_tuples():
    api = openaq.OpenAQ()
    measurements = api.measurements(city="Los Angeles", parameter='pm25')
    return [(tuple_['date']['utc'], tuple_['value']) for tuple_ in measurements[1]['results']]


def save_tuples():
    tuples = get_tuples()
    for tuple_ in tuples:
        record = Record(datetime=tuple_[0], value=tuple_[1])
        DB.session.add(record)
        DB.session.commit()


@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    tuples = [(record.datetime, record.value) for record in records]
    return f"{tuples}"


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    save_tuples()
    DB.session.commit()
    return 'Data refreshed!'
