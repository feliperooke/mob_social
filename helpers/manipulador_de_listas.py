import os
from filelock import FileLock
import subprocess


def add_lista(arquivo_in, linha):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))

    if not os.path.exists(dir_arquivo_in):
        os.makedirs(dir_arquivo_in)

    arquivo = open("{}/{}".format(dir_arquivo_in, os.path.basename(arquivo_in)), "a")
    arquivo.write(str(linha)+"\n")
    arquivo.close()


def add_lista_lock(arquivo_in, linha):

    lock = FileLock("add_lista.lock")
    with lock:
        add_lista(arquivo_in, linha)


def add_lista_if_not_in_lock(arquivo_in, linha):

    lock = FileLock("add_lista.lock")
    with lock:
        if not in_lista(arquivo_in, linha):
            add_lista(arquivo_in, linha)


def in_lista(arquivo_in, linha):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))

    if not os.path.exists(dir_arquivo_in):
        return False

    existe = False

    try:
        arquivo = open(arquivo_in, "r")
        for line in arquivo.readlines():
            if line.rstrip() == linha.rstrip():
                existe = True
                break
        arquivo.close()
    except IOError:
        pass

    return existe


def remove_lista_lock(arquivo, linha):
    lock = FileLock("add_lista.lock")
    with lock:
        remove_lista(arquivo, linha)


def remove_lista(arquivo, linha):
    subprocess.call(["sed -i '/{}/d' {}".format(linha, arquivo)], shell=True)
