import openaq
from flask import Flask

APP = Flask(__name__)


def get_tuples():
    api = openaq.OpenAQ()
    measurements = api.measurements(city="Los Angeles", parameter='pm25')
    return [(tuple_['date']['utc'], tuple_['value']) for tuple_ in measurements[1]['results']]


@APP.route('/')
def root():
    """Base view."""
    tuples = get_tuples()
    return f"{tuples}"
