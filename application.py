from pandas import read_csv

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots # Gráfico 1
import plotly.figure_factory as ff # Gráfico 2

# [X] Gráfico 1: Vendas de qualquer jogo a cada ano - Table and Chart Subplots
# [X] Gráfico 2: Vendas por gêneros - Figure Factory Subplots
# [] Gráfico 3: Vendas por região - Bubble Maps
# [] Gráfico 4: Vendas por publicadora ao longo dos anos - Line Charts
# [X] Gráfico 5: Vendas por plataforma - Sunburst

# Dados começam em 1980 e terminam em 2020

# Usar o pandas apenas para ler o arquivo csv
df = read_csv("vgsales.csv")
# Pegar cada jogo e transformar todos os seus dados em um item de uma lista chamada df_array
df_array = df.values

# ----------------------------------------------------------------------------------
# Dados 1

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
# Todos é uma array para guardar todos os anos analisados
todos = []

# Loop de 1980 a 2020
for i in range(1980, 2021):
    # O total de cada ano vai ser quantos itens com o mesmo ano iguais existem 
    total_ano = anos.count(i)
    # Guardar na lista
    anos_filtro.append(total_ano)
    todos.append(i)

# ----------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------
# Dados 2

generos = []
todos_generos= ['Sports', 'Racing', 'Role-Playing', 'Puzzle', 'Misc', 'Shooter', 'Simulation', 'Action']
# Gêneros mais populares:
# Sports, Racing, Role-Playing, Puzzle, Misc, Shooter, Simulation, Action

sports = 0
racing = 0
rpg = 0
puzzle = 0
misc = 0
fps = 0
sim = 0
action = 0

for linha in df_array:
    if linha[4] == 'Sports':
        sports += int(linha[10])
    if linha[4] == 'Racing':
        racing += int(linha[10])
    if linha[4] == 'Role-Playing':
        rpg += int(linha[10])
    if linha[4] == 'Puzzle':
        puzzle += int(linha[10])
    if linha[4] == 'Misc':
        misc += int(linha[10])
    if linha[4] == 'Shooter':
        fps += int(linha[10])
    if linha[4] == 'Simulation':
        sim += int(linha[10])
    if linha[4] == 'Action':
        action += int(linha[10])

generos.append(sports)
generos.append(racing)
generos.append(rpg)
generos.append(puzzle)
generos.append(misc)
generos.append(fps)
generos.append(sim)
generos.append(action)

tabela = [['Gênero', 'Vendas'],
            ['Esportes', sports],
            ['Corrida', racing],
            ['RPG', rpg],
            ['Puzzle', puzzle],
            ['Diversos',misc],
            ['Tiro', fps],
            ['Simulação', sim],
            ['Ação', action]]

# ----------------------------------------------------------------------------------

# Dados 5
# n deu certo ainda
plataforma = []

for linha in df_array:
    try:
        plataforma.append(linha[2].upper())
    except:
        continue
    
ps3 = plataforma.count('PS3')
computador = plataforma.count('PC')
ps4 = plataforma.count('PS4')
nes = plataforma.count('NES')
ps2 = plataforma.count('PS2')
x360 = plataforma.count('X360')
n64 = plataforma.count('N64')
xone = plataforma.count('XONE')
psp = plataforma.count('PSP')
gb = plataforma.count('GB')
atari = plataforma.count('2600')
wii = plataforma.count('WII')
ng = plataforma.count('NG')

snk = ng
nintendo = nes + n64 + gb + wii
microsoft = x360 + xone 
sony = ps3 + ps4 + ps2 + psp
plataforma = sony + microsoft + computador + nintendo + atari + snk

data = dict (
    empresas = ['plataforma', 'Sony', 'Microsoft', 'PC', 'Nintendo', 'Atari', 'SNK', 'PlayStation3', 'Computador', 'PlayStation4', 'NES', 'PlayStation2', 'Xbox360', 'Nintendo64', 'XboxOne', 'PlayStationPortable', 'GameBoy', 'Atari2600', 'NintendoWii' , 'NeoGeo'],
    consoles = ['', 'plataforma', 'plataforma','plataforma','plataforma','plataforma','plataforma', 'Sony', 'PC', 'Sony', 'Nintendo', 'Sony', 'Microsoft', 'Nintendo', 'Microsoft', 'Sony', 'Nintendo', 'Atari', 'Nintendo', 'SNK' ],
    vendas = [plataforma, sony, microsoft, computador, nintendo, atari, snk, ps3, computador, ps4, nes, ps2, x360, n64, xone, psp, gb, atari, wii, ng]) 


# ----------------------------------------------------------------------------------

'''
↑↑↑
MANIPULAÇÕES DA BASE DE DADOS
-------------------------------------------------------------------------------
PLOTLY E DASH 
↓↓↓
'''


# Quando for testar no Dash, selecionar tudo entre as aspas triplas e apertar Alt + Shift + A para des-comentar
# Inicializar o Dash na variável app
app = dash.Dash(__name__)
fig1 = make_subplots(
    rows=1, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "scatter"}]]
)
fig1.add_trace(
    go.Scatter(
        x=todos,
        y=anos_filtro,
        mode="lines",
        name="vendas anuais"
    ),
    row=1, col=1
)

fig2 = ff.create_table(tabela, height_constant=50)

trace_fig2 = go.Scatter(x=todos_generos, y=generos, xaxis='x2', yaxis='y2',
                        marker=dict(color='#9400d3'),
                        name='Vendas Globais')

fig2.add_trace(trace_fig2)

fig2['layout']['xaxis2'] = {}
fig2['layout']['yaxis2'] = {}
fig2.layout.xaxis.update({'domain': [0, .5]})
fig2.layout.xaxis2.update({'domain': [.6, 1]})
fig2.layout.yaxis2.update({'anchor': 'x2'})
fig2.layout.yaxis2.update({'title': 'Vendas'})
fig2.layout.margin.update({'t':75, 'l':50, 'r': 70})

fig2.update_layout(
    title='Vendas por gêneros',
    height=800,
    font=dict(
        family="Press Start 2P",
        size=15,
        color="RebeccaPurple"
    )
)

fig5 = px.sunburst(
    data,
    names='empresas',
    parents='consoles',
    values='vendas',
    color='empresas', hover_data=['empresas'],
    color_continuous_scale='Inferno',
    
)
fig5.layout.update({'height':800})

# Estilizar o Dash
app.layout = html.Div([
    html.H1("Teste"),

    html.Br(),
    dcc.Graph(figure = fig1),

    html.Br(),
    dcc.Graph(figure = fig2),

    html.Br(),
    dcc.Graph(figure = fig5)
])
# Rodar o Dash
if __name__ == "__main__":
    app.run_server(debug=True)
