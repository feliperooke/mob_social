import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# recebe chaves do twitter e o id do usuario e limite de friends para coleta
import sys

quantidade_de_locais_diferentes = int(sys.argv[1])
geo_time_location_in_geojson_filtered = sys.argv[2]
saida = sys.argv[3]

df = pd.read_csv(geo_time_location_in_geojson_filtered, names=["userid", "lat", "lon", "time"])

# total de tweets coletados
total_tweets = df.shape[0]

# total de users coletados
total_users = df.groupby(['userid']).size().shape[0]

# contar quantos tweets cada usuario tem
df2 = df.groupby(['userid']).size().reset_index(name='qtd_tweets')

# elimino os usuarios com apenas 1 tweet geolocalizado (esse nao se move, nao serve para analise)
df2 = df2[df2['qtd_tweets'] > 1]

total_com_mais_de_um = df2.shape[0]

total_users
total_com_mais_de_um

# estou trabalhando com x porcento dos dados
100*total_com_mais_de_um/total_users

# filtrar df pelo df2
df3 = pd.merge(df, df2, on='userid', how='inner')

# estou trabalhando com x porcento dos tweets coletados
100*df3.shape[0]/total_tweets

# analisar usuarios que sempre postam na mesma localizacao
df4 = df3.groupby(['userid', 'lat', 'lon']).size().reset_index(name='tweets_neste_local').sort_values(by=['tweets_neste_local', 'userid'])
total_tweets
df4.shape[0]
# % de localizacoes possiveis de serem aproveitadas ate aqui
100*df4.shape[0]/total_tweets

df4.describe()


x = df4.sort_values(by='tweets_neste_local')['tweets_neste_local'].values
y = np.arange(1.0, len(x)+1) / len(x)
plt.plot(x, y, marker='.', linestyle='none')

# Aqui podemos perceber que temos muitos usuarios postando de uma mesma localizacao
# esses provavelmente sao perfis de lojas e que nao servem para a analise de tracos de mobilidade
# pode ser que para um trabalho futuro seja interessante analizar apenas esses perfis
# para elimina-los, vamos agrupar por userid, dessa forma aqueles que tiverem o valor mais proximos de 1
# serao os usuarios com a menor quantidade de locais diferentes

df5 = df4.groupby(['userid']).size().reset_index(name='qtd_de_locais_diferentes')
df5.shape[0]

x = df5.sort_values(by='qtd_de_locais_diferentes')['qtd_de_locais_diferentes'].values
y = np.arange(1.0, len(x)+1) / len(x)
plt.plot(x, y, marker='.', linestyle='none')

# elimina aqueles que postaram sempre no mesmo local
df5 = df5[df5['qtd_de_locais_diferentes'] > 1]
100*df5.shape[0]/total_users

df5.describe()

# baseados nesses dados optarei por trabalhar com 50% dos dados visto que
# ha mais tracos de mobilidade neles
df5 = df5[df5['qtd_de_locais_diferentes'] >= quantidade_de_locais_diferentes]
df5.shape[0]
100*df5.shape[0]/total_users

# filtrar dataset inicial
df6 = pd.merge(df, df5, on='userid', how='inner')
100*df6.shape[0]/total_tweets

del df6['qtd_de_locais_diferentes']

df6.to_csv(saida, index=False)
del df2
del df3
del df4
del df5
