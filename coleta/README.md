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

        python -m coleta.geojson_para_bbox <geojson_in.json> <bbox_out.csv>


### Passo X: Coleta de Timeline de Usuário Específico
Informações de chaves do Twitter são necessárias como parâmetros

        python -m coleta.coleta_timeline_por_iduser <consumer_key> <consumer_secret> <acess_token> <access_token_secret> <id_user>

Exemplo de uso:

        python -m coleta.coleta_timeline_por_iduser XRFKDdnq6Y2m00nMrRyUYstcM dPiVsGK05gPajbLYt5E3d94TBeslvXMK7ZAnpTC3dMj835wOxF 84719405-q0RrudftXH9X2W2AK3Wz6WatmVgYYeTQALN6lClJs NSi33FbLa3UFOJc16QTCzBw74o9HYra7ufmb4QhzHATqF 145635516

Os resultados da captura ficam guardados nos seguintes arquivos:

```bash
├── data
│   ├── id_users_erro.csv
│   ├── id_users_nogeotagged.csv
│   ├── id_users_restrito.csv
│   └── user_timeline
│       └── <id_user>.json.gz
└── logs
    └── collect_users_timelines.<host>.log
```

No arquivo **id_users_erro.csv** ficam armazenados todos os usuários que apresentaram algum erro não conhecido no processo de coleta.

No arquivo **id_users_nogeotagged.csv** ficam armazenados todos os usuários que não tem twittes geolocalizados em sua timeline.

No arquivo **id_users_restrito.csv** ficam armazenados todos os usuários cujos perfis são de acesso restrito.

No diretorio **user_timeline** ficam armazenados em
