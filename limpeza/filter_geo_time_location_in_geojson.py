# entradas: arquivo csv com id, lat, lon, time e arquivo geojson

import conf
import pandas as pd
import logging
import os
import socket
import json
import sys
import helpers.manipulador_de_listas as mani
from shapely.geometry import shape, Point

file_locations = sys.argv[1]
file_geojson = sys.argv[2]


hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/filter_locations_in_geojson.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def filter_squares():
    # load GeoJSON file containing sectors
    with open(file_geojson) as f:
        js = json.load(f)

    df_locations = pd.read_csv(file_locations, names=["userid", "lon", "lat", "time"])

    for _, line_location in df_locations.iterrows():

        # construct point based on lon/lat returned by geocoder
        point = Point(line_location.lon, line_location.lat)

        # check each polygon to see if it contains the point
        for feature in js['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                mani.add_lista(conf.lista_filter_locations_in_geojson, "{},{},{},{}\n".format(line_location.userid,
                                                                                              line_location.lon,
                                                                                              line_location.lat,
                                                                                              line_location.time))


def filter_poligono():
    # load GeoJSON file containing sectors
    with open(file_geojson) as f:
        js = json.load(f)

    df_locations = pd.read_csv(file_locations, names=["userid", "lon", "lat", "time"])

    polygon = shape(js['geometries'][0])

    for _, line_location in df_locations.iterrows():

        # construct point based on lon/lat returned by geocoder
        point = Point(line_location.lon, line_location.lat)

        if polygon.contains(point):
            mani.add_lista(conf.lista_filter_locations_in_geojson, "{},{},{},{}".format(line_location.userid,
                                                                                        line_location.lon,
                                                                                        line_location.lat,
                                                                                        line_location.time))


filter_poligono()
