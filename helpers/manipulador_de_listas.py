from filelock import FileLock
import os
import subprocess


def add_lista(arquivo_in, linha):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))

    if not os.path.exists(dir_arquivo_in):
        os.makedirs(dir_arquivo_in)

    arquivo = open("{}/{}".format(dir_arquivo_in, os.path.basename(arquivo_in)), "a")
    arquivo.write(str(linha)+"\n")
    arquivo.close()


def add_lista_lock(arquivo_in, linha, file_lock="lock/add_lista.lock"):

    dir_file_lock = os.path.abspath(os.path.dirname(file_lock))
    if not os.path.exists(dir_file_lock):
        os.makedirs(dir_file_lock)

    lock = FileLock(file_lock)
    with lock:
        add_lista(arquivo_in, linha)


def add_lista_if_not_in_lock(arquivo_in, linha, file_lock="lock/add_lista.lock"):

    dir_file_lock = os.path.abspath(os.path.dirname(file_lock))
    if not os.path.exists(dir_file_lock):
        os.makedirs(dir_file_lock)

    lock = FileLock(file_lock)
    with lock:
        if not in_lista(arquivo_in, linha):
            add_lista(arquivo_in, linha)


def in_lista_lock(arquivo_in, linha, file_lock="lock/add_lista.lock"):

    dir_file_lock = os.path.abspath(os.path.dirname(file_lock))
    if not os.path.exists(dir_file_lock):
        os.makedirs(dir_file_lock)

    lock = FileLock(file_lock)
    na_lista = False
    with lock:
        na_lista = in_lista(arquivo_in, linha)
    return na_lista


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


def remove_lista_lock(arquivo, linha, file_lock="lock/add_lista.lock"):

    dir_file_lock = os.path.abspath(os.path.dirname(file_lock))
    if not os.path.exists(dir_file_lock):
        os.makedirs(dir_file_lock)

    lock = FileLock(file_lock)
    with lock:
        remove_lista(arquivo, linha)


def remove_lista(arquivo, linha):
    subprocess.call(["sed -i '/{}/d' {}".format(linha, arquivo)], shell=True)
