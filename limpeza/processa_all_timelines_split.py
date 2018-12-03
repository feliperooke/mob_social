# recebe chaves do twitter e o id do usuario e limite de friends para coleta
import conf
import subprocess
import logging
import os
import sys
from os import walk
import socket

n_lista = sys.argv[1]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/processa_timeline.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def processa_timeline():

    dir_timeline = "{}/user_timeline".format(conf.dir_dados)
    dir_cleaned = "{}/users_timeline_cleaned".format(conf.dir_dados)
    # lock_file = "lock/processa_timeline.lock"

    # verifica se existe a pasta, senao cria
    if not os.path.exists(dir_cleaned):
        os.makedirs(dir_cleaned)

    # entra na pasta user_timeline e lista todos os arquivos csv
    _, _, users_coletados = walk(dir_timeline).next()

    # pega apenas os ids
    users_coletados = map(lambda x: str.replace(x, ".json.gz", ""), users_coletados)

    pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    for user_id in users_coletados:

        if not os.path.isfile("{}/{}.csv".format(dir_cleaned, user_id)):
            subprocess.call(["cd {};python -m limpeza.processa_timeline_by_iduser {} {}".format(pasta_pai, user_id, n_lista)], shell=True)


processa_timeline()
