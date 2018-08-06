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


### Passo 4: Coleta de Timelines da Cidade
Nesse passo o arquivo **coleta_cidade.py** é chamado. Para ele são passados como parâmetros um arquivo contendo chaves do twitter e o arquivo gerado no passo 3. Abaixo segue o comando a ser executado:

        python -m coleta.coleta_cidade <file_keys_twitter>
        
Exemplo de uso:

        python -m coleta.coleta_cidade /<caminho_absoluto>/data/keys_twitter.csv /<caminho_absoluto>/data/london_bbox.csv

O script **coleta_cidade.py** dispara um processo para cada bbox presente no arquivo de entrada, esses processos executam o script **coleta_bbox.py** com as informações do bbox e chaves correntes. O script **coleta_bbox.py** por sua vez, faz chamadas ao **passo X** e ao **passo Y**.

### Passo 5: Coleta de Timelines de Friends e Followers da Cidade
Nesse passo o arquivo **coleta_followers_and_friends_cidade.py** é chamado. Para ele é passado como parâmetro um arquivo contendo as chaves do twitter. Esse script é responsável por executar o **passo Z**. Abaixo segue o comando a ser executado:

        python -m coleta.coleta_timeline_por_iduser <consumer_key> <consumer_secret> <acess_token> <access_token_secret> <id_user>


### Passo X: Coleta de Timeline de Usuário Específico
Informações de chaves do Twitter e id do usuário são necessários como parâmetros

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

No diretorio **user_timeline** ficam armazenados em arquivos <id_user>.json.gz toda a timeline de determinado usuário.


### Passo Y: Coleta de Friends e Followers

Informações de chaves do Twitter, id do usuário e limite da quantidade de amigos a serem coletados são necessários como parâmetros
```bash
        # Para coleta de Friends
        python -m coleta.coleta_friends_por_iduser <consumer_key> <consumer_secret> <acess_token> <access_token_secret> <id_user> <limite_de_amigos>

        # Para coleta de Followers
        python -m coleta.coleta_followers_por_iduser <consumer_key> <consumer_secret> <acess_token> <access_token_secret> <id_user> <limite_de_seguidores>
```
Exemplo de uso:
```bash    
        # Friends
        python -m coleta.coleta_friends_por_iduser XRFKDdnq6Y2m00nMrRyUYstcM dPiVsGK05gPajbLYt5E3d94TBeslvXMK7ZAnpTC3dMj835wOxF 84719405-q0RrudftXH9X2W2AK3Wz6WatmVgYYeTQALN6lClJs NSi33FbLa3UFOJc16QTCzBw74o9HYra7ufmb4QhzHATqF 145635516 500
        # Followers
        python -m coleta.coleta_folowers_por_iduser XRFKDdnq6Y2m00nMrRyUYstcM dPiVsGK05gPajbLYt5E3d94TBeslvXMK7ZAnpTC3dMj835wOxF 84719405-q0RrudftXH9X2W2AK3Wz6WatmVgYYeTQALN6lClJs NSi33FbLa3UFOJc16QTCzBw74o9HYra7ufmb4QhzHATqF 145635516 500
```
Os resultados da captura ficam guardados nos seguintes arquivos:
```bash
├── data
│   ├── id_users_friends_erro.csv
│   ├── id_users_followers_erro.csv
│   ├── id_users_restrito.csv
│   ├── user_friends
│   │   └── <id_user>.csv
│   └── user_followers
│       └── <id_user>.csv
└── logs
    ├── collect_users_friends.<host>.log
    └── collect_users_followers.<host>.log
```
No arquivo **id_users_erro.csv** ficam armazenados todos os usuários que apresentaram algum erro não conhecido no processo de coleta.

No arquivo **id_users_restrito.csv** ficam armazenados todos os usuários cujos perfis são de acesso restrito.

No diretorio **user_friends** ficam armazenados em arquivos <id_user>.csv todos os amigos de determinado usuário, se limitando ao parâmetro <limite_de_amigos>.

No diretorio **user_followers** ficam armazenados em arquivos <id_user>.csv todos os amigos de determinado usuário, se limitando ao parâmetro <limite_de_seguidores>.

### Passo Z: Coleta de Timeline de Friends e Followers
O script **coleta_friends_timeline.py** e **coleta_folowers_timeline.py** quando executados, fazem uma varredura das pastas **user_friends** e **user_followers** respectivamente, percorrendo os arquivos com os ids de amigos e seguidores coletando suas timelines. Todos os usuários cujos amigos ou seguidores já foram coletados ficam armazenados em uma lista ao final.

Os resultados da captura ficam guardados nos seguintes arquivos:
```bash
├── data
│   ├── id_users_timeline_friends_collecteds_error.csv
│   ├── id_users_timeline_followers_collecteds_error.csv
│   ├── id_users_timeline_friends_collecteds.csv
│   └── id_users_timeline_followers_collecteds.csv
│       
└── logs
    ├── collect_friends_timelines.<host>.log
    └── collect_followers_timelines.<host>.log
```
