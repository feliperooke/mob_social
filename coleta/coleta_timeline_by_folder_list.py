# a partir da lista com todos os ids de friends
# percorro essa lista disparando de 22 em 22 que e o tamanho da qtd de chaves que eu tenho
# percorro disparando o algoritimo dcoleta de timelines
# e ao mesmo tempo vou removendo os usuarios do listao assim que vou disparando

# comando: python -m coleta.coleta_timeline_by_folder_list data/keys_twitter.csv data/iduser_friends_splited 4

# recebe chaves do twitter
import sys
import conf
import logging
import os
from os import walk
import subprocess
import socket
import pandas as pd

hostname = socket.gethostname()

file_keys_twitter = sys.argv[1]
dir_listas = sys.argv[2]
processos_por_chave = int(sys.argv[3])

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_timeline_by_folder.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def coleta_timelines_by_folder():

    df_twitter = pd.read_csv(file_keys_twitter)

    # entra na pasta user_friends e lista todos os arquivos csv
    _, _, listas_de_ids = walk(dir_listas).next()

    qt_lines_twitter = df_twitter.shape[0]

    pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    contador = 0

    for lista_de_ids in listas_de_ids:

        contador = contador % qt_lines_twitter

        comando = "cd {} && nohup python -m ".format(pasta_pai)

        comando += "coleta.coleta_timeline_by_iduser_list {} {} {} {} {} {}& ".format(df_twitter.iloc[contador].consumer_key,
                                                                                      df_twitter.iloc[contador].consumer_secret,
                                                                                      df_twitter.iloc[contador].acess_token,
                                                                                      df_twitter.iloc[contador].access_token_secret,
                                                                                      "{}/{}".format(dir_listas, lista_de_ids),
                                                                                      processos_por_chave)

        contador += 1

        logging.info("[COMANDO]: {}".format(comando))

        logging.info("Executando comando")

        # faz a chamada a coleta e enquanto nao coletar a qtd total nao volta para o loop
        subprocess.call([comando], shell=True)
        logging.info("Comando finalizado")


coleta_timelines_by_folder()
