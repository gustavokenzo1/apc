from pandas import read_csv
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Gráfico 1: Vendas de qualquer jogo a cada 5 anos - Table and Chart Subplots
# Gráfico 2: Vendas por gêneros - Figure Factory Subplots
# Gráfico 3: Vendas por região - Bubble Maps
# Gráfico 4: Vendas por publicadora ao longo dos anos - Line Charts
# Gráfico 5: Vendas por plataforma - Sunburst

df = read_csv("vgsales.csv")
df_array = df.values

anos = []

for linha in df_array:
    try:
        anos.append(int(linha[3]))
    except:
        continue

# Comeca em 1980 e termina em 2020

"""
 ano_1980, ano_1985, ano_1990, ano_1995, ano_2000, ano_2005, ano_2010, ano_2015, ano_2020 = 0, 0, 0, 0, 0, 0, 0, 0, 0
ano_filtro = []

for i in range(len(anos)):
    if anos[i] >= 1980 and anos[i] < 1985:
        ano_1980 += 1
    if anos[i] >= 1985 and anos[i] < 1990:
        ano_1985 += 1
    if anos[i] >= 1990 and anos[i] < 1995:
        ano_1990 += 1
    if anos[i] >= 1995 and anos[i] < 2000:
        ano_1995 += 1
    if anos[i] >= 2000 and anos[i] < 2005:
        ano_2000 += 1
    if anos[i] >= 2005 and anos[i] < 2010:
        ano_2005 += 1
    if anos[i] >= 2010 and anos[i] < 2015:
        ano_2010 += 1
    if anos[i] >= 2015 and anos[i] < 2020:
        ano_2015 += 1
    if anos[i] == 2020:
        ano_2020 += 1

ano_filtro.append(ano_1980)
ano_filtro.append(ano_1985)
ano_filtro.append(ano_1990)
ano_filtro.append(ano_1995)
ano_filtro.append(ano_2000)
ano_filtro.append(ano_2005)
ano_filtro.append(ano_2010)
ano_filtro.append(ano_2015)
ano_filtro.append(ano_2020)

# 122, 83, 281, 1488, 3198, 6010, 4183, 961, 1

fig = px.line(x=["1", "2", "3", "4", "5", "6", "7", "8", "9"], y=ano_filtro, title="teste") 

"""
nintendo = 0
microsoft = 0
take2 = 0
sony = 0
activision = 0
empresas = []

for linha in df_array:
    if linha[5] == 'Nintendo':
        nintendo += 1
    if linha[5] == 'Microsoft Game Studios':
        microsoft += 1
    if linha[5] == 'Take-Two Interactive':
        nintendo += 1
    if linha[5] == 'Sony Computer Entertainment':
        sony += 1
    if linha[5] == 'Activision':
        activision += 1

empresas.append(nintendo)
empresas.append(microsoft)
empresas.append(take2)
empresas.append(sony)
empresas.append(activision)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Vendas a cada 5 anos"),
    html.Br(),
    dcc.Graph(figure = fig)
])

app.run_server(use_reloader = False, debug = True)