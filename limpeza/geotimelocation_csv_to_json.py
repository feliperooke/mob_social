import pandas as pd
import json
from datetime import datetime, timedelta
from email.utils import parsedate_tz
import sys

csv = sys.argv[1]
saida = sys.argv[2]


def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])


df = pd.read_csv(csv, converters={'time': to_datetime})

df = df.sort_values(by=['userid', 'time'])

estrutura = []

ultimo = None

for indice, line in df.iterrows():

    if (ultimo is None):
        ultimo = {}
        ultimo['userid'] = line.userid
        ultimo['places'] = []

        place = {}
        place['lat'] = line.lat
        place['lon'] = line.lon
        place['time'] = line.time.strftime('%Y-%m-%d %H:%M:%S')

        ultimo['places'].append(place)

    elif ultimo['userid'] == line.userid:
        place = {}
        place['lat'] = line.lat
        place['lon'] = line.lon
        place['time'] = line.time.strftime('%Y-%m-%d %H:%M:%S')

        ultimo['places'].append(place)

    else:
        estrutura.append(ultimo)

        ultimo = {}
        ultimo['userid'] = line.userid
        ultimo['places'] = []

        place = {}
        place['lat'] = line.lat
        place['lon'] = line.lon
        place['time'] = line.time.strftime('%Y-%m-%d %H:%M:%S')

        ultimo['places'].append(place)

estrutura.append(ultimo)

with open(saida, 'w') as outfile:
    json.dump(estrutura, outfile)
