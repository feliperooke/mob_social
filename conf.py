####################################
# Arquivo de configuracoes basicas #
####################################

import os

# Caminho do diretorio base da aplicacao
dir_base = os.path.abspath(os.path.dirname(__file__))

# Caminho dos logs da aplicacao
dir_logs = "{}/logs".format(dir_base)

# Caminho do diretorio de dados da aplicacao
dir_dados = "{}/data".format(dir_base)

# Caminho da lista de id_users que nao tem tweets geolocalizados
lista_nogeotagged = "{}/id_users_nogeotagged.csv".format(dir_dados)

# Caminho da lista de id_users que deram erro ao coletar
lista_erro = "{}/id_users_erro.csv".format(dir_dados)

# Caminho da lista de id_users que deram erro ao coletar
lista_friends_erro = "{}/id_users_friends_erro.csv".format(dir_dados)

# Caminho da lista de id_users que deram erro ao coletar
lista_followers_erro = "{}/id_users_followers_erro.csv".format(dir_dados)

# Caminho da lista de id_users que tem o perfil restrito
lista_restrito = "{}/id_users_restrito.csv".format(dir_dados)

# Caminho da lista de id_users que tem as timelines dos amigos coletadas
lista_friends_timelines = "{}/id_users_timeline_friends_collecteds.csv".format(dir_dados)

# Caminho da lista de id_users que tem as timelines dos amigos coletadas
lista_friends_timelines_error = "{}/id_users_timeline_friends_collecteds_error.csv".format(
    dir_dados)

# Caminho da lista de id_users que tem as timelines dos followers coletadas com erro
lista_followers_timelines = "{}/id_users_timeline_followers_collecteds.csv".format(dir_dados)

# Caminho da lista de id_users que tem as timelines dos followers coletadas com erro
lista_followers_timelines_error = "{}/id_users_timeline_followers_collecteds_error.csv".format(
    dir_dados)

# Limite defalt de amigos e seguidores coletados por usuario
limite = "5000"

# Aquivo do filtro locations in a geojson
lista_filter_locations_in_geojson = "{}/geo_time_location_in_geojson_filtered.csv".format(dir_dados)
