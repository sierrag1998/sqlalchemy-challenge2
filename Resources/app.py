import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes- Welcome Page

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )


# Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcps
    all_prcps = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcps.append(prcp_dict)

    return jsonify(all_prcps)


# Stations Route

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# Tobs Route

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates, temps for most active station in last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281',
                                                                       Measurement.date <= '2017-08-18',
                                                                       Measurement.date >= '2016-08-18').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


# Dynamic Start Date

@app.route("/api/v1.0/<start>")
def start_date_entered(start):
    session = Session(engine)

    start_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start)
    start_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start)
    start_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start)

    session.close()

    start_list = [start_min[0][0], round(start_avg[0][0], 2), start_max[0][0]]
    return jsonify(start_list)

#Dynamic Start and End Date

@app.route("/api/v1.0/<start>/<end>")
def start_end_entry(start, end):

    session = Session(engine)

    start_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)
    start_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)
    start_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)

    session.close()

    start_list = [start_min[0][0], round(start_avg[0][0], 2), start_max[0][0]]
    return jsonify(start_list)


if __name__ == '__main__':
    app.run(debug=True)