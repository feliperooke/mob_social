# Limpeza dos dados

Este diretório contém scripts que farão a limpeza dos dados para que as análises e processamentos posteriores sejam realizados.

## Processa timeline por id user
Esse script abre o arquivo data/users_timeline/< id_user >.json.gz e o processa criando um arquivo csv data/users_timeline_cleaned/<id_user>.csv e o adiciona em um arquivo contendo todos os dados de geolocalização de todos os usuários coletados data/all_geo_time_location.csv

Esses arquivos contém a seguinte estrutura:

**all_geo_time_location.csv** :

id_user | lat | lon | time
--- | --- | --- | ---
12345 | 0.000000 | 0.000000 | 2018-08-07T21:57:07+00:00


**users_timeline_cleaned/< id_user >.csv** :

lat | lon | time
--- | --- | ---
-122.07717128 | 37.36412875 | Thu Feb 05 04:09:50 +0000 2015


Exemplo de Uso:
```bash
    python -m limpeza.processa_timeline_by_iduser 1483
```

## Processa todas as timelines
Esse script chama o script que processa timeline por id user iterando sobre todos os usuários da pasta data/users_timeline/


Exemplo de Uso:
```bash
    python -m limpeza.processa_all_timelines
```
