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

# Caminho da lista de id_users que tem o perfil restrito
lista_restrito = "{}/id_users_restrito.csv".format(dir_dados)
