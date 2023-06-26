# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;when choosing your start date, please enter as yyyy-mm-dd<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;when choosing your start/end date, please enter as yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = dt.date(2017, 8, 23)
    year_ago = last_date - dt.timedelta(days=365)
    session = Session(engine)
    data1 = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date.between(year_ago,last_date)).all()
    session.close()
    prcp_dict = {}
    for date, prcp in data1:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    data2 = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(data2))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    last_date = dt.date(2017, 8, 23)
    year_ago = last_date - dt.timedelta(days=365)
    session = Session(engine)
    data3 = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date.between(year_ago,last_date)).all()
    session.close()
    tobs_dict = {}
    for date, tobs in data3:
        tobs_dict[date] = tobs
    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def begin(start):
    session = Session(engine)
    data4 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    tmin,tmax,tavg=data4[0]
    result_dict={
        "minimum temperature":tmin,
        "maximum temperature":tmax,
        "average temperature":tavg
    }
    return jsonify(result_dict)


@app.route("/api/v1.0/<start>/<end>")
def begin_end(start, end):
    session = Session(engine)
    data5 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    session.close()
    tmin,tmax,tavg=data5[0]
    result_dict={
        "minimum temperature":tmin,
        "maximum temperature":tmax,
        "average temperature":tavg
    }
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(debug=True)

