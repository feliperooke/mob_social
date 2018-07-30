# recebe chaves do twitter e o id do usuario
import gzip
import helpers.manipulador_de_listas as mani
import json
import logging
import os
import pandas as pd
import socket
import sys
import tweepy
import conf

consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
acess_token = sys.argv[3]
access_token_secret = sys.argv[4]
id_user = sys.argv[5]

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

    output_filename = "{}/{}.json.gz".format(dir_followers, user_id)

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

    # users_followers_collected_set = set()

    # users_followers_collected_output = "{}/data/user_followers.csv".format(dir_base)

    # graph_users = nx.DiGraph()

    # graph_users_output = "{}/data/graph_user.followers.adjlist".format(dir_base)

    # logging.info("User {} - Inicia leitura da lista de coletados".format(user_id))

    # users_followers_collected_set = pd.read_csv(output_filename)


    # with open(users_friends_collected_output, 'rb') as csv_file:
    #    reader = csv.reader(csv_file)
    #    for item in reader:
    #        users_friends_collected_set.extend(item)
    #    csv_file.close()

    logging.info("User {} - Finaliza leitura da lista de coletados".format(user_id))

    # Se existe o arquivo, recupera
    #if os.path.exists(users_friends_collected_output):
    #    f = gzip.open(users_friends_collected_output,'rb')
    #    users_friends_collected_set = pickle.load(f)
    #    f.close()


    #Skip user if it was already followers collected
    if user_id in users_followers_collected_set.values:
        logging.info("User {} - Already had followers collected".format(user_id))

    else:


        logging.info("User {} - Inicia leitura da lista de adjacencia/digrafo".format(user_id))

        #If graph exists, recovery
        if os.path.exists(graph_users_output):
            graph_users = nx.read_adjlist(graph_users_output, create_using=nx.DiGraph())
            #graph_users = nx.read_gpickle(graph_users_output)

        logging.info("User {} - Finaliza leitura da lista de adjacencia/digrafo".format(user_id))


        #if not in graph, add
        if user_id not in graph_users:
            logging.info("User {} - Usuario nao esta no grafo".format(user_id))
            graph_users.add_node(user_id)

        # Collect all friends of the user
        logging.info("User {} - Starting collecting followers".format(user_id))

        user_followers = []

        try:
            c = tweepy.Cursor(api.followers_ids, id=user_id)
            for page in c.pages():
                user_followers.extend(page)

        # API error
        except tweepy.RateLimitError:
            rates = api.rate_limit_status()
            rate_limit_reset = rates["resources"]["followers"]["/followers/ids"]["reset"]
            to_sleep = max(rate_limit_reset - int(time.time()), 0)
            logging.warning("User {} - Rate limit exceeded, sleeping {} seconds".format(user_id, to_sleep+1))
            time.sleep(to_sleep+1)
        except tweepy.TweepError, error:
            logging.warning("User {} - API error code: {}".format(user_id, error.message))
        except:
            e = sys.exc_info()[0]
            logging.warning("User {} - Sys Error: {}".format(user_id, e))

        logging.info("User {} - Finish collecting followers".format(user_id))

        logging.info("User {} - Starting add followers in graph".format(user_id))

        #add followers in the graph
        for user_follower_id in user_followers:
            #if is not in the graph
            if user_follower_id not in graph_users:
                #add
                graph_users.add_node(user_follower_id)
            #add edge between friend ----> user
            graph_users.add_edge(user_follower_id, user_id)

        logging.info("User {} - Finish add followers in graph".format(user_id))

        #save all and finish
        # Output result only if there was no error
        if user_followers is not None and len(user_followers) > 0:

            logging.info("User {} - Adiciona na lista de visitados".format(user_id))
            #add user in the visited set
            users_followers_collected_set.loc[len(users_followers_collected_set)] = user_id

            #save the collected set
            #with gzip.open(users_friends_collected_output,'wb') as outfile:
            #    pickle.dump(users_friends_collected_set,outfile)
            #    outfile.close()

            logging.info("User {} - Inicia gravacao da lista de visitados".format(user_id))
            #save the collected set
            #with open(users_friends_collected_output, 'wb') as csv_file:
            #    writer = csv.writer(csv_file)
            #    for value in users_friends_collected_set:
            #        writer.writerow(value)

            users_followers_collected_set.to_csv(users_followers_collected_output, index=False)


            logging.info("User {} - Finaliza gravacao da lista de visitados".format(user_id))

            #save the graph
            logging.info("User {} - Inicia gravacao do Grafo".format(user_id))
            with open(graph_users_output, 'wb') as graph_out:
                nx.write_adjlist(graph_users, graph_out)
                graph_out.close()

            logging.info("User {} - Finaliza gravacao do grafo".format(user_id))
            #nx.write_gpickle(graph_users, graph_users_output)

            logging.info("User {} - Finished ({} followers)".format(user_id, len(user_followers)))
        else:
            logging.info("User {} - Terminated".format(user_id))

        ###############################################################
        # I can collect here the tweets from friends, if necessary
        ###############################################################

        i = 0
        for user_follower in user_followers:
             if i >= 500 :
                 break
             else:
                 get_twitter_timeline(user_follower)
                 i = i + 1

    del users_followers_collected_set
    del users_followers_collected_output
    del graph_users
    del graph_users_output


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

        except Exception as e:
            # Se o erro for outro, registra e sai do loop
            logging.warning("User {} - Erro Desconhecido: {} - Reason: {} - Error: {}".format(user_id, e.message))
            coletou = True

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
                logging.warning("User {} - Erro ao gerar bytes para escrita no json".format(user_id))
        logging.info("User {} - Finished ({} tweets)".format(user_id, len(user_timeline)))
    else:
        mani.add_lista_lock(conf.lista_nogeotagged, user_id)
        logging.info("User {} - Terminated - no geotagged tweets".format(user_id))


get_twitter_timeline(id_user)
