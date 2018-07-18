import json
import helpers.manipulador_de_listas as mani
import sys

arquivo_in = sys.argv[1]
arquivo_out = sys.argv[2]

# dir_base = os.path.abspath(os.path.dirname(__file__))+"/.."
# dir_dados = "{}/data".format(dir_base)

# ler o arquivo geojson
with open(arquivo_in, "rb") as input_file:
    json_bytes = input_file.read()

    if sys.version_info[0] < 3:
        json_str = json_bytes
    else:
        json_str = json_bytes.decode('utf-8')

    data = json.loads(json_str)

    id = 0

    # percorre cada poligono pegando as coordenadas
    for forma in data:
        sw_lon = forma["geometry"]["coordinates"][0][1][0]
        sw_lat = forma["geometry"]["coordinates"][0][1][1]
        ne_lon = forma["geometry"]["coordinates"][0][3][0]
        ne_lat = forma["geometry"]["coordinates"][0][3][1]

        # adiciona as coordenadas no arquivo e salva
        mani.add_lista(arquivo_out, "{},{},{},{},{}".format(id, sw_lon, sw_lat, ne_lon, ne_lat))

        id += 1
