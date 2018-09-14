# recebe chaves do twitter e o id do usuario e limite de friends para coleta
import conf
from os import walk


def extrai_lista():

    dir_id_users_by_bbox = "{}/id_users_by_bbox".format(conf.dir_dados)

    print dir_id_users_by_bbox

    _, bbox_collected, _ = walk(dir_id_users_by_bbox).next()

    all_idusers = set()

    for bbox in bbox_collected:

        arquivo = open("{}/{}/bbox_id_users.csv".format(dir_id_users_by_bbox, bbox), "r")
        for line in arquivo.readlines():
            all_idusers.add(line.rstrip().split(",")[1])
        arquivo.close()

    arquivo = open("{}/all_idusers_collected_in_bbox.csv".format(conf.dir_dados), "a")
    for id in all_idusers:
        arquivo.write(str(id)+"\n")
    arquivo.close()


extrai_lista()
