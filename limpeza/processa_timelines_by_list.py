# recebe chaves do twitter e o id do usuario e limite de friends para coleta
import conf
import subprocess
import logging
import os
import sys
import socket

file_list_ids = sys.argv[1]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/processa_timeline.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def processa_timeline():

    dir_cleaned = "{}/users_timeline_cleaned".format(conf.dir_dados)

    pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    # verifica se existe a pasta, senao cria
    if not os.path.exists(dir_cleaned):
        os.makedirs(dir_cleaned)

    users_coletados = []

    arquivo = open(file_list_ids, "r")
    for line in arquivo.readlines():
        users_coletados.add(line.rstrip())
    arquivo.close()

    for user_id in users_coletados:
        if not os.path.isfile("{}/{}.csv".format(dir_cleaned, user_id)):
            subprocess.call(["cd {};python -m limpeza.processa_timeline_by_iduser {}".format(pasta_pai, user_id)], shell=True)


processa_timeline()
