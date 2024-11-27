# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Store last date of dataset into last_date variable, then use dt.timedelta to calculate 12 month difference and store result into last_twelve_months variable.
last_date = dt.date(2017,8,23)
last_twelve_months = last_date - dt.timedelta(days=365)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Homepage route. List all available routes.
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/[start_date]**</br>"
        f"/api/v1.0/[start_date]/[end_date]**"
        f"</br>"
        f"</br>"
        f"**Please enter date in 'YYYY-MM-DD' format</br>"
        f"Example: /api/v1.0/2011-01-01</br>"

    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query, store into results variable
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date <= last_date).\
    filter(Measurement.date >= last_twelve_months).all()

    # Close session
    session.close()

    # Establish list to append dictionaries
    prcp_list = []

    # Loop through query results, add date as key and prcp as corresponding value;
    # then, append dictionary to prcp_list
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)

    #JSONify list
    return jsonify(prcp_list)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Station.station).all()

    # Close session
    session.close()

    # Return a JSON list of stations from the dataset. Convert list of tuples to standard list
    all_stations = list(np.ravel(results))

    #JSONify list
    return jsonify(all_stations)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all temperature observations for the last 12 months for the most
    # active station -- USC00519281
    results = session.query(Measurement.tobs).\
    filter(Measurement.date <= last_date).\
    filter(Measurement.date >= last_twelve_months).\
    filter(Measurement.station == 'USC00519281').all()

    # Close session
    session.close()

    # Return a JSON list of temperature observations for the previous year. 
    # Convert list of tuples to standard list
    all_tobs = list(np.ravel(results))
    
    #JSONify list
    return jsonify(all_tobs)

# start_date route
@app.route("/api/v1.0/<start>")
def start_date(start): # User will enter start date in browser in YYYY-MM-DD format.
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create list of all dates in Measurements table
    all_dates = session.query(Measurement.date).all()
    all_dates_list = np.ravel(all_dates).tolist()

    # Conditional statement to check if user entered date is in all_dates_list.
    # If date exists:
    if start in all_dates_list:
        
        # List for querying. Use func.min, max, avg.
        sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

        # Query, store results into results variable
        results = session.query(*sel).filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

        # Close session
        session.close()

        # List for dictionaries
        list_for_dict = []

        # Loop through query results, store tmin, tmax, tavg into temp_dict
        # Add temp_dict as value to date_dict. 'date' will be the key.
        for date, tmin, tmax, tavg in results:
            date_dict = {}
            temp_dict = {}
            temp_dict['tobs_min'] = tmin
            temp_dict['tobs_max'] = tmax
            temp_dict['tobs_avg'] = round(tavg,2)
            date_dict[date] = temp_dict
            list_for_dict.append(date_dict)

        # JSONify the list
        return jsonify(list_for_dict)
    # If date is not in all_dates_list, return error message
    else: return jsonify({'error': 'date not found'}),404

# specified date_range route
@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create list of all dates in Measurements table
    all_dates = session.query(Measurement.date).all()
    all_dates_list = np.ravel(all_dates).tolist()

    # Conditional statement to check if user entered dates are in all_dates_list.
    # If date exists:
    if start in all_dates_list and end in all_dates_list:
        
        # query data into list
        sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

        # Query, stored into results
        results = session.query(*sel).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).group_by(Measurement.date).all()

        # Close session
        session.close()

        # List for dictionary results
        list_for_dict = []

        # Loop through query results, append tmin, tmax, tavg into temp_dict,
        # then add the temp_dict as value in date_dict, where the date will be a key
        for date, tmin, tmax, tavg in results:
            date_dict = {}
            temp_dict = {}
            temp_dict['tobs_min'] = tmin
            temp_dict['tobs_max'] = tmax
            temp_dict['tobs_avg'] = round(tavg,2)
            date_dict[date] = temp_dict
            list_for_dict.append(date_dict)

        # JSONify the list
        return jsonify(list_for_dict)
    # If date is not present in all_dates_list, return error message.
    else: return jsonify({'error': 'date not found'}),404

if __name__ == '__main__':
    app.run(debug=True)