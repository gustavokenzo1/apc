from pandas import read_csv
from math import isnan
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Gráfico 1: Vendas de qualquer jogo a cada ano - Table and Chart Subplots
# Gráfico 2: Vendas por gêneros - Figure Factory Subplots
# Gráfico 3: Vendas por região - Bubble Maps
# Gráfico 4: Vendas por publicadora ao longo dos anos - Line Charts
# Gráfico 5: Vendas por plataforma - Sunburst

# Dados começam em 1980 e terminam em 2020

# Usar o pandas apenas para ler o arquivo csv
df = read_csv("vgsales.csv")
# Pegar cada jogo e transformar todos os seus dados em um item de uma lista chamada df_array
df_array = df.values

# Criar array para guardar todos os anos
anos = []

# Para cada linha na df_array, pegar o ano e colocar na lista
# O try e o except servem para os jogos que não tem a informação do ano de publicação
# Quando ocorre um erro, ele simplesmente pula para o próximo jogo, ao invés de quebrar o código
for linha in df_array:
    try:
        anos.append(int(linha[3]))
    except:
        continue

# Ordernar os anos em ordem crescente
anos.sort()
# Declarar variável para contar quantos jogos foram lançados em determinado ano
total_ano = 0
# Criar array em que cada item vai ser quantos jogos foram lançados em cada ano
anos_filtro = []

todos = []

# Loop de 1980 a 2020
for i in range(1980, 2021):
    # O total de cada ano vai ser quantos itens com o mesmo ano iguais existem 
    total_ano = anos.count(i)
    # Guardar na lista
    anos_filtro.append(total_ano)
    todos.append(i)

# Mesma lógica dos anos
publicadoras = []

for linha in df_array:
    publicadoras.append(linha[5])

publicadoras_filtro = []

# Passar tudo para string, pois tem um valor "nan" que não é string
for i in range(len(publicadoras)):
    publicadoras[i] = str(publicadoras[i])

# Se a publicadora estiver not availabe or unknown, não colocar na lista
for i in range(len(publicadoras)):
    if publicadoras[i] != 'nan' and publicadoras[i] != 'Unknown':
        publicadoras_filtro.append(publicadoras[i])

# O set() filtra todos os repetidos, o key serve para o sorted saber com o que se deve ordernar, e o reversed é para ficar em ordem crescente
comum = sorted(set(publicadoras_filtro), key=publicadoras_filtro.count, reverse=True)

'''

↑↑↑
MANIPULAÇÕES DA BASE DE DADOS

-------------------------------------------------------------------------------

PLOTLY E DASH 
↓↓↓

'''

"""
Quando for testar no Dash, selecionar tudo entre as aspas triplas e apertar Alt + Shift + A para des-comentar
 # Criar o gráfico 
fig = px.line(x=todos, y=anos_filtro, title="Gráfico")

# Inicializar o Dash na variável app
app = dash.Dash(__name__)

# Estilizar o Dash
app.layout = html.Div([
    html.H1("Vendas a cada ano"),
    html.Br(),
    dcc.Graph(figure = fig)
])

# Rodar o Dash
app.run_server(use_reloader = False, debug = True) 
"""