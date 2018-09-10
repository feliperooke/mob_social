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

hostname = socket.gethostname()

consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
acess_token = sys.argv[3]
access_token_secret = sys.argv[4]
lista_coleta = sys.argv[5]
processos_por_chave = sys.argv[6]


# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_friends_timelines.{}.{}.log".format(conf.dir_logs, os.path.basename(lista_coleta), hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def coleta_all_id_friends_timelines():

    global api

    pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

    fila = []

    with open(lista_coleta, "r") as ins:
        for linha in ins:
            fila.append(linha.rstrip())

    while not (len(fila) == 0):

        comando = "cd {} &&".format(pasta_pai)
        wait = " wait"

        for contador in range(0, processos_por_chave):
            # remove o primeiro da fila
            id_user = fila.pop(0)

            # monta comando com ele
            # aqui serao enfileirados varios comandos de coleta por vez
            comando += "python -m coleta.coleta_timeline_por_iduser {} {} {} {} {}& ".format(consumer_key,
                                                                                             consumer_secret,
                                                                                             acess_token,
                                                                                             access_token_secret,
                                                                                             id_user)
            wait += " %{}".format((contador + 1))

            logging.info("Mandando user: {} com a chave: {} para a coleta no processo: {}".format(id_user, consumer_key, contador))

            # remove o id usado da pilha
            mani.remove_lista_background(lista_coleta, id_user)

            logging.info("Apagando o usuario: {} da lista em disco".format(id_user))

        comando += wait

        logging.info("[COMANDO]: {}".format(comando))

        logging.info("Executando comando")

        # faz a chamada a coleta e enquanto nao coletar a qtd total nao volta para o loop
        subprocess.call([comando], shell=True)
        logging.info("Comando finalizado")


coleta_all_id_friends_timelines()
