import conf
import logging
import os
import pandas as pd
import socket
import subprocess
import sys

file_keys_twitter = sys.argv[1]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)


print("{}/collect_friends_and_followers.{}.log".format(conf.dir_logs, hostname))

logging.basicConfig(filename="{}/collect_cidade.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

logging.info("Iniciando coleta...")

df_twitter = pd.read_csv(file_keys_twitter)

qt_lines_twitter = df_twitter.shape[0]

contador = 0
pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

for indice, line_twitter in df_twitter.iterrows():

    if((indice % 2) == 0):
        logging.info("Executando coleta do amigos utilizando a chave: {}".format(indice))
        subprocess.call(["cd {} && nohup python -m coleta.coleta_friends_timeline \
                         {} {} {} {} &".format(pasta_pai,
                                               line_twitter.consumer_key,
                                               line_twitter.consumer_secret,
                                               line_twitter.acess_token,
                                               line_twitter.access_token_secret)], shell=True)
    else:
        logging.info("Executando coleta do seguidores utilizando a chave: {}".format(indice))
        subprocess.call(["cd {} && nohup python -m coleta.coleta_followers_timeline \
                         {} {} {} {} &".format(pasta_pai,
                                               line_twitter.consumer_key,
                                               line_twitter.consumer_secret,
                                               line_twitter.acess_token,
                                               line_twitter.access_token_secret)], shell=True)
