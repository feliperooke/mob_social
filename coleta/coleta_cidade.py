import conf
import logging
import os
import pandas as pd
import socket
import subprocess
import sys

file_keys_twitter = sys.argv[1]
file_bbox = sys.argv[2]

hostname = socket.gethostname()

# inicia configuracoes de logging
if not os.path.exists(conf.dir_logs):
    os.makedirs(conf.dir_logs)


print("{}/collect_cidade.{}.log".format(conf.dir_logs, hostname))

logging.basicConfig(filename="{}/collect_cidade.{}.log".format(conf.dir_logs, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

logging.info("Iniciando coleta...")

df_twitter = pd.read_csv(file_keys_twitter)
df_bbox = pd.read_csv(file_bbox, names=["id_bbox", "sw_lon", "sw_lat", "ne_lon", "ne_lat"])

qt_lines_twitter = df_twitter.shape[0]
qt_lines_twitter

contador = 0
pasta_pai = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

for _, line_bbox in df_bbox.iterrows():
    contador = contador % qt_lines_twitter

    logging.info("Executando coleta do bbox: {} utilizando a chave: {}".format(
        int(line_bbox.id_bbox), contador))
    subprocess.call(["cd {}  && python -m coleta.coleta_bbox \
                     {} {} {} {} {} {} {} {} {} {} &".format(pasta_pai,
                                                             df_twitter.iloc[contador].consumer_key,
                                                             df_twitter.iloc[contador].consumer_secret,
                                                             df_twitter.iloc[contador].acess_token,
                                                             df_twitter.iloc[contador].access_token_secret,
                                                             int(line_bbox.id_bbox),
                                                             line_bbox.sw_lon,
                                                             line_bbox.sw_lat,
                                                             line_bbox.ne_lon,
                                                             line_bbox.ne_lat,
                                                             conf.limite)], shell=True)
    contador += 1
