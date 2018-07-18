## Passos para Realização da Coleta

### Passo 1: GeoJson
O primeiro passo é a obtenção de um arquivo geojson do local a ser explorado. Essa obtenção pode ser realizado buscando-se um arquivo pronto, de uma cidade por exemplo, ou pode ser gerado através de sites como: http://geojson.io

### Passo 2: Divisão da Área em Grids
Para que a coleta seja realizada de maneira mais homogênea é necessário subdividir a área a ser explorada. Esse passo é necessário pois ao se delimitar uma área muito grande, áreas de maior ocorrencia de posts geolocalizados podem ser privilegiadas.

Para realizar esse passo execute os comandos abaixo.

Para áreas de 100m x 100m

        hextile -s square -w 100 <geojson_in.json> <geojson_out.json>

Para áreas de 200m x 200m

        hextile -s square -w 200 <geojson_in.json> <geojson_out.json>

### Passo 3: Conversão de GeoJson para Bounding Box
Esse passo é necessário devido a especificidade da rede social trabalhada, no caso o Twitter (https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location). para essa conversão execute o comando:

        python -m coleta.geojson_to_bbox <geojson_in.json> <bbox_out.csv>
