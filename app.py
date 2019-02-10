from flask import Flask
from flask import jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(bind=engine)


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    print('Server received request for "Home" Page ....')
    return(
        f'Available Routes: <br>'
        f'/api/v1.0/precipitation'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    precip = session.query(Station.name, Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()
    return jsonify(precip)
    
@app.route('/api/v1.0/stations')
def stations():
    stations_page = session.query(Station.name).all()
    return jsonify(stations_page)

@app.route('/api/v1.0/tobs')
def temp():
    tobs = session.query(Station.name, Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).all()
    tobs = tobs[1:2250]
    return jsonify(tobs)

# got stuck at this part. 
@app.route('/api/v1.0/<start>')
def start():
    station_summary = engine.execute('SELECT measurement.station, measurement.prcp, measurement.tobs FROM measurement').fetchall()
    return jsonify(station_summary)

if __name__ == '__main__':
    app.run(debug=True)