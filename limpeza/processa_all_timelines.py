# recebe chaves do twitter e o id do usuario e limite de friends para coleta
import conf
import subprocess
import logging
import os
import sys
import socket

n_lista = int(sys.argv[1])
hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/processa_timeline.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def processa_timeline():

    pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    for num in range(0, n_lista):
        subprocess.call(["cd {} && nohup python -m limpeza.processa_all_timelines_split {} &".format(pasta_pai, num)], shell=True)


processa_timeline()
