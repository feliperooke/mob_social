import helpers.manipulador_de_listas as mani
import sys

valor = sys.argv[1]

arquivo_in = "data/teste.csv"

for i in range(0, 100000):
    mani.add_lista(arquivo_in, valor)
