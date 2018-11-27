import json
import os
import pandas as pd
from geopy import distance
import copy
import sys

estrutura_json = sys.argv[1]
# estrutura_json = "/home/rooke/Projetos/mob_social/data/filtered_local_geo_time_location_in_geojson_min_11_filtered_teste.json"
# saida_estrutura_json = sys.argv[2]
# saida_estrutura_json = "/home/rooke/Projetos/mob_social/data/filtered_local_geo_time_location_in_geojson_min_11_filtered_home.json"

dir_estrutura_json = os.path.abspath(os.path.dirname(estrutura_json))
file_estrutura_json = os.path.basename(estrutura_json)

data = None
with open(estrutura_json) as json_file:
    data = json.load(json_file)

# se a diferenca dele para o comparado for de menos que X metros
# desloco o ponto comparado para a mesma localizacao do atual
# verifico se existe uma coordenada que tem mais checkins que as demais, agrupando e ordenando da maior para a menor
# se na ordenacao a primeira tiver a mesma quantidade que a segunda, verifico qual tem mais localizacoes noturnas, de 18:00 as 3:00
# se ainda assim for igual, repito os procedimentos aumentando o raio X de comparacao


for user in data:
    print(user["userid"])

    places = copy.copy(user["places"])

    home = {}
    achouHome = False
    raioDeBusca = 0
    while(not achouHome):
        raioDeBusca += 10
        print("Raio: {}".format(raioDeBusca))
        # compara o ponto atual com todos os outros
        for i in range(0, len(places)-1):
            pontoAtual = (places[i]["lat"], places[i]["lon"])
            # se a diferenca dele para o comparado for de menos que X metros
            for j in range(i, len(places)-1):
                pontoComparado = (places[j]["lat"], places[j]["lon"])
                if(distance.distance(pontoAtual, pontoComparado).m <= raioDeBusca):
                    # desloco o ponto comparado para a mesma localizacao do atual
                    places[j]["lat"] = places[i]["lat"]
                    places[j]["lon"] = places[i]["lon"]

        # print(places)
        df = pd.DataFrame(places)
        df.time = pd.to_datetime(df.time)

        # verifico se existe uma coordenada que tem mais checkins que as demais, agrupando e ordenando da maior para a menor
        groupby = df.groupby(['lat', 'lon']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)

        # se a primeira for maior que a segunda
        if(groupby.iloc[0].counts > groupby.iloc[1].counts):
            achouHome = True
            home["lat"] = groupby.iloc[0].lat
            home["lon"] = groupby.iloc[0].lon
            print("mais checkins: {}".format(groupby.iloc[0].counts))
        else:
            # se na ordenacao a primeira tiver a mesma quantidade que a segunda,
            # verifico qual tem mais localizacoes noturnas, de 18:00 as 3:00
            # # Seleciono os que tiveram empate
            gbMax = groupby[groupby.counts == groupby.iloc[0].counts]

            # # funcao para pegar a qtd de checkins noturnos
            def qt_checkins_at_night(row):
                return len(df[(df.lat == row['lat']) &
                              (df.lon == row['lon']) &
                              ~df.time.dt.strftime('%H:%M:%S').between('03:00:00', '18:00:00')])

            # # pego a qtd de checkins noturnos de cada coordenada
            gbMax['night'] = gbMax.apply(qt_checkins_at_night, axis=1)

            # # ordeno do maior para o menor pela qtd de checkins noturnos
            gbMax = gbMax.sort_values(by=['night'], ascending=False)

            # se ainda assim for igual, repito os procedimentos aumentando o raio X de comparacao
            # se nao for, retorna a home
            if(not (gbMax.iloc[0].night == gbMax.iloc[1].night)):
                achouHome = True
                home["lat"] = gbMax.iloc[0].lat
                home["lon"] = gbMax.iloc[0].lon
                print("mais noturnos: {}".format(gbMax.iloc[0].night))
            del gbMax

        del groupby
        del df

    user["home"] = home

with open("{}/home_{}".format(dir_estrutura_json, file_estrutura_json), 'w') as outfile:
    json.dump(data, outfile)

del data
