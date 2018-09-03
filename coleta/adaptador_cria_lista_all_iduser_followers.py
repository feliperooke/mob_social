# recebe chaves de acesso as apis do twitter
# entra na pasta user_friends e acessa um a um os arquivos csv
# verifica antes de acessar se esta na lista de coletados ou se esta na lista de erros
# se esta, sai fora
# senao,adiciona na lista de erros de coleta
# e inicia a coleta da timeline dos amigos
# assim que terminar de coletar os amigos, retira da lista de erros

# recebe chaves do twitter
import sys
import conf
import helpers.manipulador_de_listas as mani
import logging
import os
from os import walk
import socket

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_followers_timelines.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def processa_all_id_followers_timelines():

    global api

    dir_followers = "{}/user_followers".format(conf.dir_dados)
    all_userid_followers = "{}/all_idusers_followers.csv".format(conf.dir_dados)

    # verifica se existe a pasta
    if not os.path.exists(dir_followers):
        logging.warning("Nao existe a pasta de coletados - Return")
        return

    # entra na pasta user_followers e lista todos os arquivos csv
    _, _, users_coletados = walk(dir_followers).next()

    # pega apenas os ids
    users_coletados = map(lambda x: str.replace(x, ".csv", ""), users_coletados)

    # percorre todos os arquivos da pasta de seguidores
    for id_user in users_coletados:
        file_id_user = "{}/{}.csv".format(dir_followers, id_user)
        try:
            # entra dentro de todos os arquivos e pega os ids
            arquivo = open(file_id_user, "r")
            for line in arquivo.readlines():
                id_user_timeline = line.rstrip()
                # add os ids em um listao
                mani.add_lista(all_userid_followers, id_user_timeline)

        except IOError as e:
            logging.error("User {} - Erro Desconhecido: {}".format(id_user, e.message))


processa_all_id_followers_timelines()