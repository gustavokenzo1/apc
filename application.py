from pandas import read_csv # pip install pandas

import dash # pip install dash
import dash_core_components as dcc # pip install dash-core-components
import dash_html_components as html # pip install dash-html-components
import dash_bootstrap_components as dbc # pip install dash-boostrap-components

import plotly.express as px #pip install plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff # Gráfico 2

# [X] Gráfico 1: Vendas de qualquer jogo a cada ano - Bar Charts
# [X] Gráfico 2: Vendas por gêneros - Figure Factory Subplots
# [X] Gráfico 3: Vendas por região - Bubble Maps
# [] Gráfico 4: Vendas por publicadora que não fabricam consoles ao longo dos anos - Line Charts
# [X] Gráfico 5: Vendas por plataforma - Sunburst

# Dados começam em 1980 e terminam em 2020

# Usar o pandas apenas para ler o arquivo csv
df = read_csv("vgsales.csv")
# Pegar cada jogo e transformar todos os seus dados em um item de uma lista chamada df_array
df_array = df.values

"""

Manipulação dos dados + Plotly

"""

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


# Gráfico 1
fig1 = px.bar(x=todos, y=anos_filtro)

fig1.update_layout(
    title='Vendas por ano',
    template='plotly_dark'
)

# ----------------------------------------------------------------------------------
# Dados 2

generos = []
todos_generos= ['Esportes', 'Corrida', 'RPG', 'Puzzle', 'Diversos', 'Tiro', 'Simulação', 'Ação']
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

# Para cada jogo, pegar o número de vendas globais (índice 10 no csv) e ir somando de acordo com o gênero do jogo
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

# Guardar o número de vendas numa array para usar no gráfico de linhas 
generos.append(sports)
generos.append(racing)
generos.append(rpg)
generos.append(puzzle)
generos.append(misc)
generos.append(fps)
generos.append(sim)
generos.append(action)

# Criação da tabela
# A primeira linha indica o nome de cada coluna
# As linhas seguintes associam o nome do gênero ao número de vendas
tabela = [['Gênero', 'Vendas'],
            ['Esportes', sports],
            ['Corrida', racing],
            ['RPG', rpg],
            ['Puzzle', puzzle],
            ['Diversos',misc],
            ['Tiro', fps],
            ['Simulação', sim],
            ['Ação', action]]


# Gráfico 2
# ff foi importado
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
        size=15,
        color="RebeccaPurple"
    ),
    template='plotly_dark'
)


# ----------------------------------------------------------------------------------
# Dados 3

# North America, European Union, Japan
lat = [44.76, 50.03, 37.36, -15.96]
long = [-99.53, 10.14, 139.34, -5.70]
vendas_na = 0
vendas_eu = 0
vendas_jp = 0
vendas_outros = 0
vendas_3 = []
regions = ['América do Norte', 'União Européia', 'Japão', 'Outros']

# 1763 NA
# 837 EU
# 406 JP

for linha in df_array:
    vendas_na += int(linha[6])
    vendas_eu += int(linha[7])
    vendas_jp += int(linha[8])
    vendas_outros += int(linha[9])

vendas_3.append(vendas_na)
vendas_3.append(vendas_eu)
vendas_3.append(vendas_jp)
vendas_3.append(vendas_outros)


# Gráfico 3
limits = [(400, 600), (700, 900), (1500, 2000), (2200, 5000)]
cores = ["green", "royalblue", "crimson", "yellow"]

fig3 = go.Figure()
scale = 50

for i in range(len(limits)):
    lim = limits[i]

    fig3.add_trace(go.Scattergeo(
                    lon = (long[i],lat),
                    lat = (lat[i],long),
                    marker = dict(
                        size = vendas_3[i]/scale,
                        color = cores[i],
                        line_color = 'rgb(40,40,40)',
                        line_width = 0.5,
                        sizemode = 'area'
                    ),
                    name = '{0}'.format(regions[i]),
    ))

fig3.update_layout(
    title_text = 'Vendas por região',
    showlegend = True,
    geo = dict(
        landcolor = 'rgb(217, 217, 217)'
    ),
    template='plotly_dark',
    autosize=True
)


# ----------------------------------------------------------------------------------
# Dados 4

# 5 Publicadoras que mais publicaram e não fabricam consoles
publicadoras_apenas = ['Electronic Arts', 'Activision', 'Namco Bandai Games', 'Ubisoft', 'Konami Digital Entertainment']

anos_4 = []
ubisoft = []
ea = []
activision = []
take_two = []
bandai_namco = []

for i in range(1980, 2021, 5):
    anos_4.append(i)

for i in range(1980, 2021, 5):

    ubisoft_ = ea_ = activision_ = take_two_ = bandai_namco_ = 0

    for linha in df_array:
        if linha[5] == 'Ubisoft' and linha[3] == float(i):
            ubisoft_ += linha[10]

        if linha[5] == 'Electronic Arts' and linha[3] == float(i):
            ea_ += linha[10]

        if linha[5] == 'Activision' and linha[3] == float(i):
            activision_ += linha[10]
                
        if linha[5] == 'Take-Two Interactive' and linha[3] == float(i):
            take_two_ += linha[10]

        if linha[5] == 'Namco Bandai Games' and linha[3] == float(i):
            bandai_namco_ += linha[10]

    ubisoft.append(ubisoft_)
    ea.append(ea_)
    activision.append(activision_)
    take_two.append(take_two_)
    bandai_namco.append(bandai_namco_)

publicadoras_4 = []
publicadoras_4.append(ubisoft)
publicadoras_4.append(ea)
publicadoras_4.append(take_two)
publicadoras_4.append(activision)
publicadoras_4.append(bandai_namco)

# Gráfico 4

fig4 = go.Figure()

for i in range(5):
    fig4.add_trace(go.Scatter(x=anos_4, y=publicadoras_4[i - 1], mode='lines+markers', name=publicadoras_apenas[i - 1]))

fig4.update_traces(hoverinfo='name+y')
fig4.update_layout(title='Vendas por Publicadoras de Jogos',
                   template='plotly_dark')

# ----------------------------------------------------------------------------------

# Dados 5
plataforma = []

# Guardar a plataforma de cada jogo numa array chamada plataforma
for linha in df_array:
    try:
        plataforma.append(linha[2].upper())
    except:
        continue

# Contar quantos jogos foram publicados para cada console
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

# Fazer as associações como se fosse uma regra da cadeia
# Plataforma contém todas as empresas
# Cada empresa engloba seus consoles
snk = ng
nintendo = nes + n64 + gb + wii
microsoft = x360 + xone 
sony = ps3 + ps4 + ps2 + psp
plataforma = sony + microsoft + computador + nintendo + atari + snk

# Dict = dicionário
# Em consoles, colocar primeiro as empresas e depois os consoles
# Em empresas, colocar "plataforma" nas mesmas posições em que existe uma empresa na lista acima e,
# em seguida, colocar o nome da empresa na mesma posição de cada console dessa empresa
# Em vendas, colocar o valor de vendas, que vai determinar o tamanho de cada setor do gráfico
data = dict (
    consoles = ['Plataforma', 'Sony', 'Microsoft', 'PC', 'Nintendo', 'Atari', 'SNK', 'PlayStation 3', 'Computador', 'PlayStation4', 'NES', 'PlayStation 2', 'Xbox 360', 'Nintendo 64', 'Xbox One', 'PSP', 'GameBoy', 'Atari2600', 'Nintendo Wii' , 'NeoGeo'],
    empresas = ['', 'Plataforma', 'Plataforma','Plataforma','Plataforma','Plataforma','Plataforma', 'Sony', 'PC', 'Sony', 'Nintendo', 'Sony', 'Microsoft', 'Nintendo', 'Microsoft', 'Sony', 'Nintendo', 'Atari', 'Nintendo', 'SNK' ],
    vendas = [plataforma, sony, microsoft, computador, nintendo, atari, snk, ps3, computador, ps4, nes, ps2, x360, n64, xone, psp, gb, atari, wii, ng]) 


# Gráfico 5
fig5 = px.sunburst(
    data,
    names='consoles',
    parents='empresas',
    values='vendas',
    template='plotly_dark'
    
)
fig5.layout.update({'height':800})

"""

Dash

"""

# Quando for testar com o Dash, selecionar tudo entre as aspas triplas e apertar Alt + Shift + A para des-comentar
# Inicializar o Dash na variável app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Estilizar o Dash
# Layout do Dash, sempre que quiser fazer o gráfico aparecer, colocar aqui
app.layout = html.Div(
    
    className="div-principal", children=[

    html.H1("Grupo 4 - Vendas de Jogos"), # H1 = Heading 1, ou cabeçalho
    html.Br(),
    html.H5("Observação: todos os dados estão em milhões de unidades"),

    html.Br(), # Br =  break, ou quebra de linha, para deixar mais espaçado
    dcc.Graph(figure = fig1),

    html.Br(),
    dcc.Graph(figure = fig2),

    html.Br(),
    dcc.Graph(figure = fig3),

    html.Br(),
    dcc.Graph(figure = fig4),

    html.Br(),
    dcc.Graph(figure = fig5)
])

# Rodar o Dash
# Para ficar mais dinâmico, basta deixar o código rodando apertar Ctrl + S para salvar,
# O Dash vai atualizar sozinho a cada 5 segundos +-, ou vc pode só clicar em reload mesmo
if __name__ == "__main__":
    app.run_server(debug=True)
