

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.extautomap import automap_base
from sqlalchemy.orm import Session
from sqlalchelmy import create_endgine, func, inspect
import numpy as np

#create engine to connect to database

engine= create_engine("sqlite://Resources/hawaii.sqlite")

app= Flask(__name__)

@app.rout("/")
def welcome():
    return (
            f"Hawaii Temps API!<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end<br/>")


@app.route("/api/v.10/precipitation")
def precipitation():

    conn = engine.connect()

    query = '''
        SELECT
            date, 
            AVG(prcp) as avg_prcp
        
        FROM
            measurement
        WHERE
            date >= (SELECT DATE(MAX(date), '-1 year')FROM measurement)
        GROUP BY
            date
        ORDER BY
            date

'''

    prcp_df = pd.read_sql(query, conn)

    prcp_df['date] = pd.to_datetime(prcp_df['date'])

    prcp_df.sort_values('date')


    