# recebe chaves de acesso as apis do twitter
# entra na pasta user_friends e acessa um a um os arquivos csv
# verifica antes de acessar se esta na lista de coletados ou se esta na lista de erros
# se esta, sai fora
# senao,adiciona na lista de erros de coleta
# e inicia a coleta da timeline dos amigos
# assim que terminar de coletar os amigos, retira da lista de erros

# chama com python -m adaptador_divide_lista_all_iduser_friends 400000

# recebe chaves do twitter
import sys
import conf
import helpers.manipulador_de_listas as mani
import logging
import os
import socket

hostname = socket.gethostname()
qtd_por_arquivo = int(sys.argv[1])

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_friends_timelines.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")


def divide_lista():

    global api

    dir_friends_splited = "{}/iduser_friends_splited".format(conf.dir_dados)
    all_userid_friends = "{}/all_idusers_friends_v2.csv".format(conf.dir_dados)

    # verifica se existe a pasta
    if not os.path.exists(dir_friends_splited):
        os.makedirs(dir_friends_splited)

    mani.divide_lista_metodo_2(all_userid_friends, dir_friends_splited, qtd_por_arquivo)


divide_lista()
