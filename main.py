import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def separateAnswers():
  print('----------------------------------')


separateAnswers()
#Alterei a ordem das respostas para fazer mais sentido na construção da resolução, peço desculpas

#Requisito 1 - Escolher uma base de dados de sua preferência (escolhi o '10,000 Movies Data(1915-2023)' do kaggle)
# - Top 10,000 movies listed on IMDb.
pathNameFull = 'movies_data_full.csv'

dfMoviesFull = pd.read_csv(pathNameFull, index_col=0)
print(dfMoviesFull)
separateAnswers()

#Requisito 2.1 - Utilizar a função fillna, drop ou dropna (utilizei a função drop)
#Pergunta: Como remover uma coluna do dataset que não será utilizada?
# - Dropei a coluna 'Description' pois não irei utiliza-la nessa análise
#Requisito 7 - Exportar um dataframe para um novo CSV, não sendo igual ao original
#Pergunta: Como exportar um dataframe para um novo arquivo CSV?
dfMoviesFull.drop('Description', axis=1).to_csv('movies_data_filtered.csv')

pathNameFiltered = 'movies_data_filtered.csv'

dfMovies = pd.read_csv(pathNameFiltered, index_col=0)
print(dfMovies)
separateAnswers()

#Requisito 2.3 - Utilizar a função rename
#Pergunta: Como renomear as colunas desse dataset de modo que seja possível usar dot notation com todas e como fazer isso para mais de uma coluna ao mesmo tempo?
# - Renomeando determinadas colunas para remover o espaço no nome e poder usar dot notation e deixando os nomes mais autoexplicativos
columnsRenameDict = {
    'Movie Name': 'Movie_name',
    'Year of Release': 'Release_year',
    'Run Time in minutes': 'Run_time(minutes)',
    'Movie Rating': 'IMDb_rating',
    'Votes': 'IMDb_votes',
}
dfMovies = dfMovies.rename(columnsRenameDict, axis=1)
print(dfMovies)
separateAnswers()

#Requisito 3 - Realizar duas manipulações aritméticas na base de dados
# Pergunta: Qual o valor do MetaScore na escala do rating IMDb?
# - Utilizei divisão, multiplicação e soma para responder, por isso considerei que fiz mais de duas operações aritméticas, mesmo sendo para uma só coluna
# - Como o rating IMDb vai de 1 até 10 e o MetaScore de 0 até 100, foi necessário realizar operações além de dividir por 10 o valor do MetaScore
# - Assim, como o MetaScore vai de 0 a 100, sua nota já é uma porcentagem, que eu apliquei no intervalo de 1 até 10 do IMDb (que é 9) e somei 1, pois já inicia no 1
# - Obs: filmes sem MetaScore não receberam valores
dfMovies['MetaScore_To_IMDb'] = ((dfMovies.MetaScore / 100) * 9) + 1
print(dfMovies.MetaScore_To_IMDb)
separateAnswers()


#Requisito 2.2 - Utilizar a função apply
#Requisito 4 (1 de 2) - Criar uma nova coluna a partir de um dado estatístico (média)
#Pergunta: Qual é a média entre rating IMDb e MetaScore de cada filme? Para filme sem MetaScore, atribua o valor do IMDb_rating para essa nova coluna.
def iMDbMetaScoreMean(row):
  if pd.isna(row.MetaScore):
    return row.IMDb_rating
  return (row.MetaScore_To_IMDb + row.IMDb_rating) / 2


dfMovies['Average_rating'] = dfMovies.apply(iMDbMetaScoreMean, axis=1)
print(dfMovies.Average_rating)
separateAnswers()

#Requisito 4 (2 de 2) - Criar uma nova coluna a partir de um dado estatístico (porcentagem do gross sobre gross total)
#Pergunta: Dentre os filmes que possuem faturamento, apresenta a porcentagem do faturamento deles em relação ao total.
dfMovies['Percentage'] = (dfMovies.Gross / dfMovies.Gross.sum()) * 100
print(dfMovies.Percentage)
separateAnswers()

#Requisito 5 - Filtrar dados que sejam relevantes (usei o query)
#Pergunta: Como apresentar apenas os filmes que possuem faturamento, removendo os que não tem, sem utilizar 'dropna'?
dfMoviesNoNaNGross = dfMovies.query('Gross > 0')
print(dfMoviesNoNaNGross.Gross)
separateAnswers()

#Requisito 9 - Utilizar o pd.qcut ou pd.cut
#Pergunta: Qual a quantidade de filmes em cada intervalo, de 1 a 10 com 1 de incremento, no rating IMDb e na média dos dois ratings?
ratingBins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
iMDbRatingCut = pd.cut(dfMoviesNoNaNGross.IMDb_rating, bins=ratingBins)
averageRatingCut = pd.cut(dfMoviesNoNaNGross.Average_rating, bins=ratingBins)
print(iMDbRatingCut.value_counts().sort_index())
separateAnswers()
print(averageRatingCut.value_counts().sort_index())
separateAnswers()

#Requisito 6 - Utilizar o groupby, gerando alguma constatação estatística interessante
#Pergunta: Qual a média de faturamento dos filmes nos intervalos definidos no requisito 9 e o que é possível concluir?
agroupmentByIMDbRating = dfMoviesNoNaNGross.groupby(
    iMDbRatingCut, observed=False).Gross.mean().sort_index(ascending=False)
print(agroupmentByIMDbRating)
separateAnswers()
agroupmentByAverageRating = dfMoviesNoNaNGross.groupby(
    averageRatingCut, observed=False).Gross.mean().sort_index(ascending=False)
print(agroupmentByAverageRating)
separateAnswers()
# - Assim, é possível observar que levando em consideração o IMDb rating, o faturamento dos filmes no intervalo de 8 a 9 e de 9 a 10 é
# -- muito superior em comparação em quando se considera o average rating, que apresenta um faturamento melhor distribuido
# -- por entre os intervalos de rating. Vale notar também que nesse filtro, os filmes com rating 8 a 9 são o que possuem a maior média
# -- de faturamento
# Obs: embora funcionasse, o groupby apresentava um Future warning alegando que o parâmetro 'observed' iria mudar o default de False para True
# -- Para resolver, adicionei o argumento 'observed=False' explicitamente

#Requisito 8 - Gerar um gráfico a partir de qualquer dataframe utilizado no programa (matplotlib)
#Pergunta: Mostre, em um gráfico de barras, os valores dos faturamentos dos dois agrupamentos calculados por faixa de rating.
agroupmentByIMDbRating.plot(kind='bar',
                            position=1,
                            width=0.25,
                            color='c',
                            label='aaaa')
agroupmentByAverageRating.plot(kind='bar',
                               position=0,
                               width=0.25,
                               color='k',
                               label='bbbb')
plt.xlabel('Ratings')
plt.ylabel('Gross')
plt.title('Gross of ratings')
plt.show()
