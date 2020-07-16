# IMPORT DEPENDENCIES
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
# -----------------------------------------------

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()



app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Data API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(bind=engine)
    
    rain_data = session.query(Measurements.date, Measurements.prcp).\
    filter(Measurements.station == Stations.station).\    
    order_by(Measurements.date).all()
    
    session.close()

    precipitation = {}
    for date, prcp in rain_data:
        precipitation["date"] = date
        precipitation["precipitation"] = prcp
        precipitation.append(rain_dict)
        # Need to append dict with `date` as the key and `prcp` as the value.

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(bind=engine)
    station_names = session.query(Stations.name).all()
    session.close()

    return jsonify(station_names)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(bind=engine)
    
    startdate = '2016-08-23'

    most_active_stn_year_data = session.query(Measurements.date, Measurements.tobs).\
    filter(Measurements.station == Stations.station).\
    filter(Stations.id == "7").\
    filter(Measurements.date > startdate).\
    order_by(Measurements.date).all()

    session.close()

    waihee_temps = []
    for date, tobs, name in  most_active_stn_year_data:
        tobs_waihee_dict = {}
        tobs_waihee_dict["date"] = date
        tobs_waihee_dict["temperature"] = tobs
        waihee_temps.append(tobs_waihee_dict)

    return jsonify(waihee_temps)



@app.route("/api/v1.0/<start>/<end>")
def date():
    session = Session(bind=engine)
    

    return (
        f"Write your preferred date in yyyy-mm-dd format."
    )

# Need to finish app route for date filters

if __name__ == "__main__":
    app.run(debug=True)