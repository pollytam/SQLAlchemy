import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import pandas as pd
import numpy as np
from flask import Flask, jsonify
import datetime as dt

# Flask Setup
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

Measurement = base.classes.measurement
Station = base.classes.station

session = Session(engine)


@app.route("/")
def welcome():
    """Flask API"""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    prev_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    df = pd.DataFrame(session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > prev_yr).all())

    results_df = pd.DataFrame(df, columns=['date', 'precipitation'])
    results_df.set_index('date', inplace=True)

    results_dict = results_df.reset_index().to_dict('data')

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    # All stations
    stations = session.query(Station.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    prev_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\

    results_df = pd.DataFrame(results, columns=['date', 'temperature'])
    results_df.set_index('date', inplace=True)

    results_dict = results_df.reset_index().to_dict('data')

    return jsonify(results_dict)

@app.route("/api/v1.0/<start>")
def start(start=None):

    start = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    group_by(Measurement.date).all()

    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def between(start=None, end=None):

    between = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    group_by(Measurement.date).all()

    return jsonify(between)
