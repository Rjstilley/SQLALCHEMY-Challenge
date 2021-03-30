
import sys
from flask import Flask, jsonify
import sqlalchemy
# from sqlalchemy.extautomap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd

# create engine to connect to database
import os
# sets base folder to current folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# conn = engine.connect()

# # query = '''
# #             SELECT
# #                 s.station AS station_code,
# #                 s.name AS station_name

# #             FROM
# #                 measurement m
# #             INNER JOIN station s
# #             ON m.station = s.station
# #             GROUP B
# #                 s.station,
# #                 s.name
# #         '''

# active_stations_df = pd.read_sql("SELECT name FROM station", conn)

# # print(active_stations_df)

# active_stations_json = active_stations_df.to_json(orient='records')
# print(active_stations_json)

# conn.close()
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Hawaii Temps API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():

    conn = engine.connect()

    query = "SELECT * FROM measurement"

    # query = '''
#         SELECT
#             date,
#             AVG(prcp) as avg_prcp

#         FROM
#             measurement
#         WHERE
#             date >= (SELECT DATE(MAX(date), '-1 year')FROM measurement)
#         GROUP BY
#             date
#         ORDER BY
#             date

# '''

    prcp_df = pd.read_sql(query, conn)

    # prcp_df['date'] = pd.to_datetime(prcp_df['date'])

    # prcp_df.sort_values('date')

    prcp_json = prcp_df.to_json(orient='records')
    conn.close()

    print(prcp_json, file=sys.stderr)

    return prcp_json


@app.route('/api/v1.0/stations')
def station():

    conn = engine.connect()

    query = "SELECT name FROM station"

    active_stations_df = pd.read_sql(query, conn)

    # print(active_stations_df)

    active_stations_json = active_stations_df.to_dict("records")
    print(active_stations_json)

    conn.close()

    return jsonify(active_stations_json)


@app.route('/api/v1.0/tobs')
def measurement():

    conn = engine.connect()

    # query = '''

    #     SELECT
    #         s.station AS station_code,
    #         s.name AS station_name,
    #         COUNT(*) AS station_count
    #     FROM
    #         measurement m
    #     INNER JOIN station s
    #     ON m.station = s.station
    #     GROUP BY
    #         s.station,
    #         s.name
    #     ORDER BY
    #         station_count DESC
    # '''
    # active_stations_df = pd.read_sql(query, conn)
    # active_stations_df.sort_values(
    #     'station_Count', ascending=False, inplace=True)
    # most_active_station = active_stations_df['station_code'].values[0]

    # query = f'''
    #     SELECT
    #         tobs
    #     FROM
    #         measurement
    #     WHERE
    #         station = '{most_active_station}'

    #         AND

    #         date>= (SELECT DATE(MAX(date)), '-1 year') FROM measurement)

    # '''
    query = " SELECT * FROM measurement"
    mas_tobs_df = pd.read_sql(query, conn)

    mas_tobs_json = mas_tobs_df.to_json(orient='records')

    conn.close()

    return mas_tobs_json


@app.route('/api/v1.0/<start>/<end>')
def date_stat_bounded(start, end):
    conn = engine.connect()

    query = f'''
        SELECT
            MIN(tobs) AS TMIN,
            MAX(tobs) AS TMAX,
            AVG(tobs) AS TAVG
        FROM
            measurement
        WHERE
            date BETWEEN '{start}' AND {end}'
    '''

    bounded_date_stats_df = pd.read_sql(query, conn)

    bounded_date_stats_json = bounded_date_stats_df.to_json(orient='records')

    conn.close()

    return bounded_date_stats_json


@app.route('/api/v1.0/<start>')
def date_stat_open(start):

    conn = engine.connect()

    query = f'''
        SELECT
            MIN(tobs) AS TMIN,
            MAX(tobs) AS TMAX,
            AVG(tobs) AS TAVG
        FROM
            measurement

        WHERE
            date>= '{start}'

    '''

    open_date_stats_df = pd.read_sql(query, conn)

    open_date_stats_json = open_date_stats_df.to_json(orient='records')

    conn.close()
    return open_date_stats_json


if __name__ == '__main__':
    app.run(debug=True)
