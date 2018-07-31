# recebe chaves do twitter e o id do usuario
import conf
import gzip
import helpers.manipulador_de_listas as mani
import json
import logging
import os
import socket
import sys
import tweepy

consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
acess_token = sys.argv[3]
access_token_secret = sys.argv[4]
id_user = sys.argv[5]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_users_timelines.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

logging.info("Use api key - {}".format(api.auth.consumer_key))


def get_twitter_timeline(user_id):
    # https://twitter.com/intent/user?user_id=145635516

    global api

    dir_timelines = "{}/user_timeline".format(conf.dir_dados)

    if not os.path.exists(dir_timelines):
        os.makedirs(dir_timelines)

    output_filename = "{}/{}.json.gz".format(dir_timelines, user_id)

    # Skip user if it was already collected
    if os.path.exists(output_filename):
        logging.info("User {} - Skipped".format(user_id))
        return

    # Skip user if it was already in nogeotagged list
    if mani.in_lista(conf.lista_nogeotagged, user_id):
        logging.info("User {} - Skipped - in nogeotagged".format(user_id))
        return

    # Skip user if it was already in restrict list
    if mani.in_lista(conf.lista_restrito, user_id):
        logging.info("User {} - Skipped - in restrict list".format(user_id))
        return

    # Skip user if it was already collected but crashed
    if mani.in_lista(conf.lista_erro, user_id):
        logging.info("User {} - Skipped - in erro list".format(user_id))
        return

    # Senao existe usuario coletado...
    logging.info("User {} - Starting".format(user_id))

    # Add na lista de processados
    mani.add_lista_lock(conf.lista_erro, user_id)

    user_timeline = []

    coletou = False
    while not coletou:
        try:
            # tenta recuperar a pagina, se nao conseguir 2 coisas podem acontecer
            # 1 - excedeu o limite de paginas
            # 2 - excedeu o limite de requisicoes a cada 15 min
            c = tweepy.Cursor(api.user_timeline, id=user_id, trim_user=True,
                              exclude_replies=False, include_rts=True, count=200)
            for page in c.pages():
                geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
                user_timeline.extend(geotagged_tweets)

            coletou = True

            mani.remove_lista(conf.lista_erro, user_id)

        except tweepy.TweepError as e:

            if e.response is not None:
                if e.response.status_code is not None:

                    # Se excedeu o numero de requisicoes
                    if e.response.status_code == 429:
                        user_timeline = []
                        logging.warning("User {} - Error Status: {} - Reason: {} - Error: {}".format(
                            user_id, e.response.status_code, e.response.reason, e.response.text))
                        logging.warning(
                            "User {} - Coletando novamente".format(user_id))
                    else:
                        # Se perfil restrito
                        if e.response.status_code == 401:
                            mani.add_lista(conf.lista_restrito, user_id)
                        # Se o erro for outro, registra e sai do loop
                        logging.warning("User {} - Error Status: {} - Reason: {} - Error: {}".format(
                            user_id, e.response.status_code, e.response.reason, e.response.text))

                        coletou = True

                        mani.remove_lista(conf.lista_erro, user_id)
                        return

        except Exception as e:
            # Se o erro for outro, registra e sai do loop
            logging.error(
                "User {} - Erro Desconhecido: {}".format(user_id, e.message))
            coletou = True
            return

    # Se foram coletados tweets geolocalizados...
    if user_timeline is not None and len(user_timeline) > 0:
        with gzip.open(output_filename, "w") as outfile:
            try:
                # se python 2.7
                if sys.version_info[0] < 3:
                    dump = str(json.dumps(user_timeline))
                else:
                    dump = bytes(json.dumps(user_timeline), "UTF-8")
                outfile.write(dump)
            except Exception:
                logging.error(
                    "User {} - Erro ao gerar bytes para escrita no json".format(user_id))
        logging.info("User {} - Finished ({} tweets)".format(user_id, len(user_timeline)))
    else:
        mani.add_lista_lock(conf.lista_nogeotagged, user_id)
        logging.warning("User {} - Terminated - no geotagged tweets".format(user_id))


get_twitter_timeline(id_user)
