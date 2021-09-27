import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

from pandas import read_csv

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])





# Criar o primeiro gráfico
fig1 = go.Figure(
    layout={"template":"plotly_dark"}
    )

# Colocar informações no primeiro gráfico
fig1.add_trace(
    go.Scatter(
        x=todos, y=anos_filtro
        ))

# Mudar o estilo do primeiro gráfico
fig1.update_layout(
    title='Vendas de jogos por ano',
    autosize=True
)






# Layout da dashboard
# Cada gráfico que for sendo criado, deve-se adicionar uma dbc.Col com ele
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            
            html.Div([
            html.H1("Grupo 4 - Vendas de Jogos")
        ], style={"margin-top":"30px", "margin-bottom":"30px"}),

        dcc.Graph(id='grafico_de_linhas', figure=fig1)
        ]),
    ])
)

if __name__ == "__main__":
    app.run_server(debug=True)