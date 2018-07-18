import os


def add_lista(arquivo_in, linha):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))

    if not os.path.exists(dir_arquivo_in):
        os.makedirs(dir_arquivo_in)

    arquivo = open("{}/{}".format(dir_arquivo_in, os.path.basename(arquivo_in)), "a")
    arquivo.write(str(linha)+"\n")
    arquivo.close()
