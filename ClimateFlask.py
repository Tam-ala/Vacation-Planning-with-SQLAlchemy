# import libraries
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# make a connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
# Create an app, by passing __name__
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp_start<br/>"
        f"/api/v1.0/temp_startend"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of Hawaii precipitation and date"""
    # Query all precipitation measurements. Wait a few seconds to load.
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of weather stations in Hawaii"""
    # Query stations
    station = session.query(Station.station).all()

    session.close()
    
    # Convert list of tuples to normal list
    station_list = list(np.ravel(station))
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations of the most active station (Station USC00519281) in Hawaii of the last year of data"""
    # Query the dates and temperature observations from Station USC00519281.
    temps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-24').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    session.close()

    return jsonify(temps)

@app.route("/api/v1.0/temp_start")
def temp_start():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start."""
    # Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    temp_start = session.query(Measurement.station, func.min(Measurement.tobs), 
                    func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                    filter(Measurement.station >='2017-06-20').all()

    session.close()

    return jsonify(temp_start)

@app.route("/api/v1.0/temp_startend")
def temp_startend():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range."""
    # Calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    temp_startend = session.query(Measurement.station, func.min(Measurement.tobs), 
                    func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date >='2017-06-20').\
                    filter(Measurement.date <='2017-06-30').all()
   
    session.close()

    return jsonify(temp_startend)

if __name__ == '__main__':
    app.run(debug=True)