# Recebe chaves, bbox e limite de coleta como parametros
# faz um loop para coletar todas as ocorrencias de tweets geolocalizados
# assim que achar, coleta timeline do user, friends e followers de acordo com o limite especificado
# e adiciona em uma lista o id_bbox, id_user coletado

import conf
import helpers.manipulador_de_listas as mani
import logging
import os
import socket
import subprocess
import sys
import tweepy

consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
acess_token = sys.argv[3]
access_token_secret = sys.argv[4]
id_bbox = int(sys.argv[5])
sw_lon = float(sys.argv[6])
sw_lat = float(sys.argv[7])
ne_lon = float(sys.argv[8])
ne_lat = float(sys.argv[9])
limite = int(sys.argv[10])

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_bbox.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

logging.info("Use api key - {}".format(api.auth.consumer_key))


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # We only collect geotagged tweets.
        if status.geo:

            # coleta tweets
            pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
            subprocess.call(["cd {} && python -m coleta.coleta_timeline_por_iduser {} {} {} {} {}".format(pasta_pai,
                                                                                                          consumer_key,
                                                                                                          consumer_secret,
                                                                                                          acess_token,
                                                                                                          access_token_secret,
                                                                                                          status.user.id
                                                                                                          )], shell=True)
            # coleta friends
            subprocess.call(["cd {0}  && python -m coleta.coleta_friends_por_iduser {1} {2} {3} {4} {5} {6} \
                              & python -m coleta.coleta_followers_por_iduser {1} {2} {3} {4} {5} {6}".format(pasta_pai,
                                                                                                             consumer_key,
                                                                                                             consumer_secret,
                                                                                                             acess_token,
                                                                                                             access_token_secret,
                                                                                                             status.user.id,
                                                                                                             limite
                                                                                                             )], shell=True)
            # add id_bbox e id_user na lista
            try:
                mani.add_lista_if_not_in_lock("{}/id_users_by_bbox/{}/bbox_id_users.csv".format(conf.dir_dados, id_bbox),
                                              "{},{}".format(id_bbox, status.user.id),
                                              file_lock="lock/bbox_{}.lock".format(id_bbox))
            except Exception as e:
                logging.error("Erro ao add na lista bbox: {}".format(e.message))

    def on_error(self, status_code):
        logging.error("Encountered error with status code: {}".format(sys.stderr))
        # Don't kill the stream
        return True

    def on_timeout(self):
        logging.error("Timeout...: {}".format(sys.stderr))
        # Don't kill the stream
        return True


def main():
    while True:
        try:
            sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
            sapi.filter(locations=[sw_lon, sw_lat, ne_lon, ne_lat])
        except Exception as e:
            logging.error("Erro Desconhecido: {}".format(e.message))


main()
