# recebe chaves do twitter e o id do usuario e limite de friends para coleta
import conf
import helpers.manipulador_de_listas as mani
import gzip
import json
import logging
import os
import os.path
import socket
import sys

id_user = sys.argv[1]
# num_lista = sys.argv[2]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/processa_timeline.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def processa_timeline():

    dir_timeline = "{}/user_timeline".format(conf.dir_dados)
    timeline_file_user = "{}/{}.json.gz".format(dir_timeline, id_user)
    dir_cleaned = "{}/users_timeline_cleaned".format(conf.dir_dados)
    # all_geo_time_location = "{}/{}_all_geo_time_location.csv".format(num_lista, conf.dir_dados)
    # lock_file = "lock/processa_timeline.lock"

    # verifica se existe user coletado
    if not os.path.isfile(timeline_file_user):
        logging.warning("Arquivo {} nao existe, saindo do processamento...".format(timeline_file_user))
        return

    # verifica se existe a pasta, senao cria
    if not os.path.exists(dir_cleaned):
        os.makedirs(dir_cleaned)

    # abre o arquivo do usuario
    with gzip.open(timeline_file_user, "rb") as input_file:
        json_bytes = input_file.read()

        if sys.version_info[0] < 3:
            json_str = json_bytes
        else:
            json_str = json_bytes.decode('utf-8')

        # extrai o json
        data = json.loads(json_str)

        # dados = []

        # percorre os tweets extraindo as coordenadas,
        # mas antes verifica se ele ja nao foi processado anteriormente
        if not os.path.isfile("{}/{}.csv".format(dir_cleaned, id_user)):
            for tweet in data:
                # dados.append([tweet["coordinates"]["coordinates"][0],
                #              tweet["coordinates"]["coordinates"][1],
                #              tweet["created_at"]])

                linha = "{},{},{}".format(tweet["coordinates"]["coordinates"][1],
                                          tweet["coordinates"]["coordinates"][0],
                                          tweet["created_at"].replace('"', ''))

                # grava arquivo individual
                mani.add_lista("{}/{}.csv".format(dir_cleaned, id_user), linha)
                # grava no arquivao
                # mani.add_lista("{}".format(all_geo_time_location), "{},{}".format(id_user, linha))


processa_timeline()
