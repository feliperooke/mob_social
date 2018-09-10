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


def remove_lista_background(arquivo, linha):
    subprocess.call(["sed -i '/{}/d' {} &".format(linha, arquivo)], shell=True)


def first_line(arquivo_in):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))

    if not os.path.exists(dir_arquivo_in):
        return

    with open(arquivo_in, "r") as f:
        for linha in f:
            linha = linha.rstrip()
            if(linha != ""):
                print(linha)
                break
        print(linha)
    return linha


def lista_is_empty(arquivo_in):
    return os.stat(arquivo_in).st_size == 0


def divide_lista_metodo_1(arquivo_in, folder_out, divisor):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))
    if not os.path.exists(dir_arquivo_in):
        return

    dir_folder_out = os.path.abspath(folder_out)
    if not os.path.exists(dir_folder_out):
        return

    arquivos = []

    for i in range(0, divisor):
        arquivos.append(open("{}/{}.{}".format(dir_folder_out, i, os.path.basename(arquivo_in)), "a"))

    arq_principal = open(arquivo_in, 'r')

    contador = 0

    for line in arq_principal.readlines():
        # o valor de contador roda entre 0, 1, 2 ... quantidade
        contador = contador % divisor
        arquivos[contador].write(line)
        contador += 1

    arq_principal.close()

    for i in range(0, divisor):
        arquivos[i].close()


def divide_lista_metodo_2(arquivo_in, folder_out, qt_por_arquivo):

    dir_arquivo_in = os.path.abspath(os.path.dirname(arquivo_in))
    if not os.path.exists(dir_arquivo_in):
        return

    dir_folder_out = os.path.abspath(folder_out)
    if not os.path.exists(dir_folder_out):
        return

    arq_principal = open(arquivo_in, 'r')

    contador = 0
    num_arquivo = 0
    arquivo = open("{}/{}.{}".format(dir_folder_out, num_arquivo, os.path.basename(arquivo_in)), "a")

    print(qt_por_arquivo)

    for line in arq_principal.readlines():

        if contador < qt_por_arquivo:
            arquivo.write(line)
            contador += 1
        else:
            arquivo.close()
            num_arquivo += 1
            contador = 0
            arquivo = open("{}/{}.{}".format(dir_folder_out, num_arquivo, os.path.basename(arquivo_in)), "a")

    if not arquivo.closed:
        arquivo.close()

    arq_principal.close()
