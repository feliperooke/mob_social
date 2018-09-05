# a partir da lista com todos os ids de friends
# percorro essa lista disparando de 22 em 22 que e o tamanho da qtd de chaves que eu tenho
# percorro disparando o algoritimo dcoleta de timelines
# e ao mesmo tempo vou removendo os usuarios do listao assim que vou disparando

# recebe chaves do twitter
import sys
import conf
import helpers.manipulador_de_listas as mani
import logging
import os
import subprocess
import socket
import pandas as pd

hostname = socket.gethostname()

file_keys_twitter = sys.argv[1]


# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_all_friends_timelines.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def coleta_all_id_friends_timelines():

    global api

    all_userid_friends = "{}/all_idusers_friends_v2.csv".format(conf.dir_dados)

    df_twitter = pd.read_csv(file_keys_twitter)

    qt_lines_twitter = df_twitter.shape[0]

    pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    while (not mani.lista_is_empty(all_userid_friends)):

        comando = "cd {} &&".format(pasta_pai)
        wait = " wait"

        for contador in range(0, qt_lines_twitter):
            # pega o primeiro da pilha
            id_user = mani.first_line(all_userid_friends)

            # monta comando com ele
            # aqui serao enfileirados varios comandos de coleta por vez
            comando += "python -m coleta.coleta_timeline_por_iduser {} {} {} {} {}& ".format(df_twitter.iloc[contador].consumer_key,
                                                                                             df_twitter.iloc[contador].consumer_secret,
                                                                                             df_twitter.iloc[contador].acess_token,
                                                                                             df_twitter.iloc[contador].access_token_secret,
                                                                                             id_user)
            wait += " %{}".format((contador + 1))

            logging.info("Mandando user: {} para a coleta usando a chave numero: {}".format(id_user, contador))

            # remove o id usado da pilha
            mani.remove_lista(all_userid_friends, id_user)

            logging.info("Apagando o usuario: {} da lista".format(id_user))

        comando += wait

        logging.info("[COMANDO]: {}".format(comando))

        logging.info("Executando comando")

        # faz a chamada a coleta e enquanto nao coletar a qtd total nao volta para o loop
        subprocess.call([comando], shell=True)
        logging.info("Comando finalizado")


coleta_all_id_friends_timelines()
