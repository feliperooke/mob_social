# Limpeza dos dados

Este diretório contém scripts que farão a limpeza dos dados para que as análises e processamentos posteriores sejam realizados.

## Processa timeline
Esse script abre todos os arquivos do diretório data/users_timeline e processa um a um criando um arquivo csv data/users_timeline_cleaned/<id_user>.csv e um arquivo contendo todos os dados de geolocalização de todos os usuários coletados data/all_geo_time_location.csv

Esses arquivos contém a seguinte estrutura:

**all_geo_time_location.csv** :

id_user | lat | lon | time
--- | --- | --- | ---
12345 | 0.000000 | 0.000000 | 2018-08-07T21:57:07+00:00


**users_timeline_cleaned/< id_user >.csv** :

lat | lon | time
--- | --- | ---
0.000000 | 0.000000 | 2018-08-07T21:57:07+00:00
