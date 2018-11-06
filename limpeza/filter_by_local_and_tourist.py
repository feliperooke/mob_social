# separa quem e local e quem e turistas
# se o cara teve ao menos duas postagens dentro de um periodo de mais de 30 dias no intervalo de 1 ano

import json
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# estrutura_json = sys.argv[1]
estrutura_json = "/home/rooke/Projetos/mob_social/data/geo_time_location_in_geojson_min_11_filtered.json"
# limite = int(sys.argv[2])
limite = 30

dir_estrutura_json = os.path.abspath(os.path.dirname(estrutura_json))
dir_estrutura_json
file_estrutura_json = os.path.basename(estrutura_json)

data = None
with open(estrutura_json) as json_file:
    data = json.load(json_file)

date_format = '%Y-%m-%d %H:%M:%S.%f'

estrutura_local = []
estrutura_tourist = []

for user in data:

    ultima_loc = datetime.strptime(user["places"][-1]["time"], date_format)
    primeira_loc = datetime.strptime(user["places"][0]["time"], date_format)
    delta = ultima_loc - primeira_loc
    user["delta"] = delta.days

    first_time = None
    last_time = None
    deltas_by_year = {}
    max_delta = 0
    for i, place in enumerate(user["places"]):
        time_geo = datetime.strptime(user["places"][i]["time"], date_format)

        if time_geo.year not in deltas_by_year:
            deltas_by_year[time_geo.year] = 0
        else:
            time_geo_anterior = datetime.strptime(user["places"][i-1]["time"], date_format)
            delta = time_geo - time_geo_anterior
            deltas_by_year[time_geo.year] = deltas_by_year[time_geo.year] + delta.days

        if deltas_by_year[time_geo.year] > max_delta:
            max_delta = deltas_by_year[time_geo.year]

    user["deltas_by_year"] = deltas_by_year
    user["max_delta"] = max_delta

    if max_delta <= limite:
        estrutura_tourist.append(user)
    else:
        estrutura_local.append(user)

df = pd.Series((u["max_delta"] for u in data))

x = df.sort_values().values
y = np.arange(1.0, len(x)+1) / len(x)
plt.plot(x, y, marker='.', linestyle='none')


print "Encontrados {} turistas.".format(len(estrutura_tourist))
print "Encontrados {} locais.".format(len(estrutura_local))


with open("{}/filtered_local_{}".format(dir_estrutura_json, file_estrutura_json), 'w') as outfile:
    json.dump(estrutura_local, outfile)

with open("{}/filtered_tourist_{}".format(dir_estrutura_json, file_estrutura_json), 'w') as outfile:
    json.dump(estrutura_tourist, outfile)

del estrutura_json
del estrutura_local
del estrutura_tourist
