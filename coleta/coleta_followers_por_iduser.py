# recebe chaves do twitter e o id do usuario e limite de followers para coleta
import conf
import helpers.manipulador_de_listas as mani
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
limit_followers = int(sys.argv[6])

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)

logging.basicConfig(filename="{}/collect_users_followers.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

logging.info("Use api key - {}".format(api.auth.consumer_key))


def collect_users_followers(user_id):

    global api

    dir_followers = "{}/user_followers".format(conf.dir_dados)

    if not os.path.exists(dir_followers):
        os.makedirs(dir_followers)

    output_filename = "{}/{}.csv".format(dir_followers, user_id)

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

    # Collect all friends of the user
    logging.info("User {} - Starting collecting followers".format(user_id))

    # Add na lista de erros e quando a coleta finalizar retira
    mani.add_lista_lock(conf.lista_erro, user_id)

    user_followers = []

    coletou = False
    while not coletou:
        try:
            # tenta recuperar a pagina, se nao conseguir 2 coisas podem acontecer
            # 1 - excedeu o limite de paginas
            # 2 - excedeu o limite de requisicoes a cada 15 min
            c = tweepy.Cursor(api.followers_ids, id=user_id)
            for page in c.pages():
                logging.info("User {} - Coletando {} followers".format(user_id, len(page)))
                user_followers.extend(page)
                # caso exceda o limite de seguidores definidos para a coleta pare de coletar
                if len(user_followers) >= limit_followers:
                    break

            if(len(user_followers) == 0):
                logging.warning("User {} - Nao tem followers".format(user_id))

            coletou = True
            mani.remove_lista(conf.lista_erro, user_id)

        except tweepy.TweepError as e:

            if e.response is not None:
                if e.response.status_code is not None:

                    # Se excedeu o numero de requisicoes
                    if e.response.status_code == 429:
                        user_followers = []
                        logging.warning("User {} - Error Status: {} - Reason: {} - Error: {}".format(
                            user_id, e.response.status_code, e.response.reason, e.response.text))
                        logging.warning("User {} - Coletando novamente".format(user_id))
                    else:
                        # Se perfil restrito
                        if e.response.status_code == 401:
                            mani.add_lista(conf.lista_restrito, user_id)
                        # Se o erro for outro, registra e sai do loop
                        logging.warning("User {} - Error Status: {} - Reason: {} - Error: {}".format(
                            user_id, e.response.status_code, e.response.reason, e.response.text))

                        mani.remove_lista(conf.lista_erro, user_id)
                        return

        except Exception as e:
            # Se o erro for outro, registra e sai do loop
            logging.error("User {} - Erro Desconhecido: {}".format(user_id, e.message))
            return

    # GRAVA FOLLOWERS
    try:
        # add followers in the file
        i = 0
        for user_follower_id in user_followers:
            mani.add_lista(output_filename, user_follower_id)
            i += 1
            if i >= limit_followers:
                break

        if(len(user_followers) == 0):
            mani.add_lista(output_filename, "")

    except Exception:
        logging.error("User {} - Erro ao escrever no arquivo do followers do usuario".format(user_id))

    logging.info("User {} - Finish add followers in file".format(user_id))

    del user_followers


collect_users_followers(id_user)
