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
# [X] Gráfico 4: Vendas por editoras a cada 5 anos - Line Charts
# [X] Gráfico 5: Vendas por plataforma - Sunburst

# Dados começam em 1980 e terminam em 2016

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

# Declarar variável para contar quantos jogos foram lançados em determinado ano
total_ano = 0
# Criar array em que cada item vai ser quantos jogos foram lançados em cada ano
anos_filtro = []
# Todos é uma array para guardar todos os anos analisados
todos = []

# Loop de 1980 a 2016
for i in range(1980, 2016):
    # O total de cada ano vai ser quantos itens com o mesmo ano iguais existem 
    total_ano = anos.count(i)
    # Guardar na lista
    anos_filtro.append(total_ano)
    todos.append(i)


# Gráfico 1
fig1 = px.bar(x=todos, y=anos_filtro)

fig1.update_layout(
    title='Vendas Globais por Ano',
    template='plotly_dark',
    xaxis={'title': 'Anos'},
    yaxis={'title': 'Vendas'}
)

fig1.update_traces(
    hovertemplate='Vendas: %{y} <br> Ano: %{x}'
)
# ----------------------------------------------------------------------------------
# Dados 2

generos = []
todos_generos= ['Esportes', 'Corrida', 'RPG', 'Puzzle', 'Diversos', 'Tiro', 'Simulação', 'Ação']
# Gêneros mais populares:
# Sports, Racing, Role-Playing, Puzzle, Misc, Shooter, Simulation, Action

sports = racing = rpg = puzzle = misc = fps = sim = action = 0

# Para cada jogo, pegar o número de vendas globais (índice 10 no csv) e ir somando de acordo com o gênero do jogo

for linha in df_array:
    if linha[4] == 'Sports':
        sports += linha[10]

    if linha[4] == 'Racing':
        racing += linha[10]

    if linha[4] == 'Role-Playing':
        rpg += linha[10]

    if linha[4] == 'Puzzle':
        puzzle += linha[10]

    if linha[4] == 'Misc':
        misc += linha[10]                     

    if linha[4] == 'Shooter':
        fps += linha[10]

    if linha[4] == 'Simulation':
        sim += linha[10]

    if linha[4] == 'Action':
        action += linha[10]

# Guardar o número de vendas numa array para usar no gráfico de linhas 
generos.append(int(sports))
generos.append(int(racing))
generos.append(int(rpg))
generos.append(int(puzzle))
generos.append(int(misc))
generos.append(int(fps))
generos.append(int(sim))
generos.append(int(action))

# Criação da tabela
# A primeira linha indica o nome de cada coluna
# As linhas seguintes associam o nome do gênero ao número de vendas
tabela = [['Gênero', 'Vendas'],
            ['Esportes', int(sports)],
            ['Corrida', int(racing)],
            ['RPG', int(rpg)],
            ['Puzzle', int(puzzle)],
            ['Diversos', int(misc)],
            ['Tiro', int(fps)],
            ['Simulação', int(sim)],
            ['Ação', int(action)]]


# Gráfico 2
# ff foi importado para criar tabela
fig2 = ff.create_table(tabela)

fig2.add_trace(go.Scatter(x=todos_generos, y=generos, 
                        xaxis='x2', yaxis='y2',
                        marker=dict(color='#9400d3'),
                        name='Vendas Globais'))

# Inicializar eixos x e y
fig2['layout']['xaxis2'] = {}
fig2['layout']['yaxis2'] = {}

fig2.update_layout(
    title='Vendas por Gêneros',
    height=800,
    font=dict(
        size=15
    ),
    margin=dict(
        t=75,
        l=60,
        r=70,
        b=75
    ),
    xaxis=dict(
        domain=[0, 0.5] # Comprimento da tabela (0.5 significa que ocupa metade do espaço)
    ),
    xaxis2=dict(
        domain=[.6, 1] # Altera a largura do gráfico de linhas
    ),
    yaxis2=dict(
        anchor='x2', # Ancorar o título ao eixo x2 do gráfico de linhas
        title='Vendas'
    ),
    template='plotly_dark'
)


# ----------------------------------------------------------------------------------
# Dados 3

# North America, European Union, Japan, Ilha de Santa Helena
lat = [44.76, 50.03, 37.36, -15.96]
long = [-99.53, 10.14, 139.34, -5.70]
vendas_na = vendas_eu = vendas_jp = vendas_outros = 0
vendas_3 = []

# Para colocar na legenda
regions = ['América do Norte', 'União Européia', 'Japão', 'Outros']

# Contar as vendas em cada região de todos os jogos
for linha in df_array:
    vendas_na += linha[6]
    vendas_eu += linha[7]
    vendas_jp += linha[8]
    vendas_outros += linha[9]

vendas_3.append(int(vendas_na))
vendas_3.append(int(vendas_eu))
vendas_3.append(int(vendas_jp))
vendas_3.append(int(vendas_outros))


# Gráfico 3

# Cores uai
cores = ["green", "royalblue", "crimson", "yellow"]

# Inicializar o gráfico
fig3 = go.Figure()
# Escala para dividir a área e deixar em um tamanho bom
scale = 100

for i in range(len(regions)):
    fig3.add_trace(go.Scattergeo(
                    lon = (long[i],lat),
                    lat = (lat[i],long),
                    marker = dict(
                        # Tamanho de cada bolha
                        size = vendas_3[i]/scale,
                        # 'i'ésima cor da lista
                        color = cores[i],
                        # Contorno da bolha
                        line_color = 'rgb(60,60,60)',
                        # Expessura do contorno em pixels
                        line_width = 1,
                        sizemode = 'area'
                    ),
                    # Nomes na legenda
                    name = '{0}'.format(regions[i]),
                    # Quando passar o mouse em cima, aparecer legenda formatada
                    hovertemplate='Vendas: {0}'.format(vendas_3[i])
    ))

fig3.update_layout(
    title_text = 'Vendas por Região',
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

for i in range(1980, 2016, 5):

    # Guardar os anos de 5 em 5 na lista
    anos_4.append(i)

    # Inicializar variáveis para 0
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

# publicadoras_4 é uma lista de listas 
publicadoras_4 = []
publicadoras_4.append(ubisoft)
publicadoras_4.append(ea)
publicadoras_4.append(take_two)
publicadoras_4.append(activision)
publicadoras_4.append(bandai_namco)

# Gráfico 4

fig4 = go.Figure()

for i in range(len(publicadoras_apenas)):
    fig4.add_trace(go.Scatter(x=anos_4, y=publicadoras_4[i - 1], mode='lines+markers', name=publicadoras_apenas[i - 1]))

fig4.update_traces(hoverinfo='name+y+x', 
                   hovertemplate=None
                   )

fig4.update_layout(title='Vendas por Editoras a Cada 5 Anos',
                   template='plotly_dark', 
                   hovermode='x unified'
                   )

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
    template='plotly_dark',
    title='Vendas por Plataformas das 5 Maiores Empresas'
    
)

fig5.update_layout(
    height=800,
    font=dict(
        color='#fff'
    )
)
"""

Dash

"""

# Quando for testar com o Dash, selecionar tudo entre as aspas triplas e apertar Alt + Shift + A para des-comentar
# Inicializar o Dash na variável app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SLATE],
                title='Vendas de Jogos'
                )

# Estilizar o Dash
# Layout do Dash, sempre que quiser fazer o gráfico aparecer, colocar aqui
app.layout = html.Div(
    className='div-principal',
    children=[
        html.Br(),
        html.Header(className='cabecalho',
            children=[
                dbc.Row(
                    [
                        dbc.Col(html.Div(children=[html.H1("Grupo 4 - Vendas de Jogos"),
                                        html.Br(),
                                        html.H5("(todos os dados estão em milhões de unidades)")])), # H1 = Heading 1, ou cabeçalho
                        dbc.Col(html.Div(html.Img(src='assets/logo.png')),
                        )
                    ]
                ),
                html.Br(),
                ]
        ),

        html.Main(
            children=[
                html.Div(
                    id='graph-1',
                    children=[
                        html.Br(),
                        dcc.Graph(figure = fig1)
                    ]
                ),
                html.Div(
                    id='graph-2',
                    children=[
                        dcc.Graph(figure = fig2)
                    ]
                ),
                html.Div(
                    id='graph-3',
                    children=[
                        dcc.Graph(figure = fig3)
                    ]
                ),
                html.Div(
                    id='graph-4',
                    children=[
                        dcc.Graph(figure = fig4)
                    ]
                ),
                html.Div(
                    id='graph-5',
                    children=[
                        dcc.Graph(figure = fig5)
                    ]
                )
            ]
        )
    ]
)


# Rodar o Dash
# Para ficar mais dinâmico, basta deixar o código rodando apertar Ctrl + S para salvar,
# O Dash vai atualizar sozinho a cada 5 segundos +-, ou vc pode só clicar em reload mesmo
if __name__ == "__main__":
    app.run_server(debug=True)
