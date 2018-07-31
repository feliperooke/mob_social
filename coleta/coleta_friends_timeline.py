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
import subprocess
import tweepy

consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
acess_token = sys.argv[3]
access_token_secret = sys.argv[4]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_friends_timelines.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

logging.info("Use api key - {}".format(api.auth.consumer_key))


def coleta_friends_timelines():

    global api

    dir_friends = "{}/user_friends".format(conf.dir_dados)
    lock_file = "friends_timelines.lock"

    # verifica se existe a pasta
    if not os.path.exists(dir_friends):
        logging.warning("Nao existe a pasta de coletados - Return")
        return

    # entra na pasta user_friends e lista todos os arquivos csv
    _, _, users_coletados = walk(dir_friends).next()

    # pega apenas os ids
    users_coletados = map(lambda x: str.replace(x, ".csv", ""), users_coletados)

    # percorre um a um verificando se seus amigos ja foram coletados
    for id_user in users_coletados:

        # verifica antes de acessar se esta na lista de coletados ou se esta na lista de erros
        # se esta, sai fora
        if mani.in_lista_lock(conf.lista_friends_timelines_error, id_user, lock_file):
            logging.warning("User {} - timelines de friends com erro ou em processo de coleta".format(id_user))
            return

        if mani.in_lista_lock(conf.lista_friends_timelines, id_user, lock_file):
            logging.warning("User {} - timelines de friends ja coletadas".format(id_user))
            return

        logging.info("User {} - Iniciando coleta das timelines friends".format(id_user))

        # senao,adiciona na lista de erros de coleta
        mani.add_lista_lock(conf.lista_friends_timelines_error, id_user, lock_file)

        # e inicia a coleta da timeline dos amigos
        # abre arquivo com ids de amigos
        # percorre fazendo chamada ao script de coleta de timeline
        file_id_user = "{}/{}.csv".format(dir_friends, id_user)
        pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
        try:
            arquivo = open(file_id_user, "r")
            for line in arquivo.readlines():
                id_user_timeline = line.rstrip()
                subprocess.call(["cd {};python -m coleta.coleta_timeline_por_iduser {} {} {} {} {}".format(pasta_pai,
                                                                                                           consumer_key,
                                                                                                           consumer_secret,
                                                                                                           acess_token,
                                                                                                           access_token_secret,
                                                                                                           id_user_timeline)], shell=True)
            arquivo.close()
        except IOError as e:
            logging.error("User {} - Erro Desconhecido: {}".format(id_user, e.message))

        # assim que terminar de coletar os amigos, retira da lista de erros
        mani.remove_lista_lock(conf.lista_friends_timelines_error, id_user, lock_file)
        # e adiciona na lista de users_coletados
        mani.add_lista_lock(conf.lista_friends_timelines, id_user, lock_file)

        logging.info("User {} - Coleta das timelines friends finalizada".format(id_user))


coleta_friends_timelines()
