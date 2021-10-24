from pandas import read_csv  # pip install pandas

import dash  # pip install dash
import dash_core_components as dcc  # pip install dash-core-components
import dash_html_components as html  # pip install dash-html-components
from dash.dependencies import Input, Output

import plotly.express as px  # pip install plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff  # Gráfico 2

# [X] Gráfico 1: Vendas de qualquer jogo a cada ano - Bar Charts
# [X] Gráfico 2: Vendas por gêneros - Figure Factory Subplots
# [X] Gráfico 3: Vendas por região - Bubble Maps
# [X] Gráfico 4: Vendas por editoras a cada 5 anos - Line Charts
# [X] Gráfico 5: Vendas por plataforma - Sunburst

# Dados começam em 1980 e terminam em 2016

# Usar o pandas apenas para ler o arquivo csv
df = read_csv("./data/vgsales.csv")
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

order = ['Crescente', 'Decrescente', 'Cronológico']

# ----------------------------------------------------------------------------------
# Dados 2

generos = []
todos_generos = ['Esportes', 'Corrida', 'RPG',
                 'Puzzle', 'Diversos', 'Tiro', 'Simulação', 'Ação']
# Gêneros mais populares:
# Sports, Racing, Role-Playing, Puzzle, Misc, Shooter, Simulation, Action

sports = racing = rpg = puzzle = misc = fps = sim = action = 0

# Para cada jogo, pegar o número de vendas globais (índice 10 no csv) e ir somando de acordo com o gênero do jogo

for linha in df_array:
    if linha[4] == 'Sports':
        sports += linha[10]

    elif linha[4] == 'Racing':
        racing += linha[10]

    elif linha[4] == 'Role-Playing':
        rpg += linha[10]

    elif linha[4] == 'Puzzle':
        puzzle += linha[10]

    elif linha[4] == 'Misc':
        misc += linha[10]

    elif linha[4] == 'Shooter':
        fps += linha[10]

    elif linha[4] == 'Simulation':
        sim += linha[10]

    elif linha[4] == 'Action':
        action += linha[10]

# Guardar o número de vendas numa array para usar no gráfico de linhas5,
generos.append(sports)
generos.append(racing)
generos.append(rpg)
generos.append(puzzle)
generos.append(misc)
generos.append(fps)
generos.append(sim)
generos.append(action)

generos = [int(genero) for genero in generos]

# Criação da tabela
# A primeira linha indica o nome de cada coluna
# As linhas seguintes associam o nome do gênero ao número de vendas

tabela = [['Gênero', 'Vendas'],
          ['Esportes', generos[0]],
          ['Corrida', generos[1]],
          ['RPG', generos[2]],
          ['Puzzle', generos[3]],
          ['Diversos', generos[4]],
          ['Tiro', generos[5]],
          ['Simulação', generos[6]],
          ['Ação', generos[7]]]


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
    height=600,
    width=1050,
    font=dict(
        size=17
    ),
    margin=dict(
        t=75,
        l=60,
        r=70,
        b=75
    ),
    xaxis=dict(
        # Comprimento da tabela (0.5 significa que ocupa metade do espaço)
        domain=[0, 0.5]
    ),
    xaxis2=dict(
        anchor='y2',
        domain=[.6, 1]  # Altera a largura do gráfico de linhas
    ),
    yaxis2=dict(
        anchor='x2',  # Ancorar o título ao eixo x2 do gráfico de linhas
        title='Vendas'
    ),
    paper_bgcolor='rgba(233,233,233,0)',
    plot_bgcolor='rgba(20,20,20,0.3)',
    font_color='white'
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
cores = ["MediumPurple", "LightSkyBlue", "crimson", "limegreen"]

# Inicializar o gráfico
fig3 = go.Figure()
# Escala para dividir a área e deixar em um tamanho bom
scale = 70

for i in range(len(regions)):
    fig3.add_trace(go.Scattergeo(
        lon=(long[i], lat),
        lat=(lat[i], long),
        marker=dict(
            # Tamanho de cada bolha
            size=vendas_3[i]/scale,
            # 'i'ésima cor da lista
            color=cores[i],
            # Mudar a opacidade de acordo com a quantidade de vendas
            opacity=1-0.15*i,
            # Contorno da bolha
            line_color='rgb(80,80,80)',
            # Expessura do contorno em pixels
            line_width=1,
            sizemode='area'
        ),
        # Nomes na legenda
        name='{0}'.format(regions[i]),
        # Quando passar o mouse em cima, aparecer legenda formatada
        hovertemplate='Vendas: {0}'.format(vendas_3[i])
    ))

fig3.update_layout(
    title_text='Vendas por Região',
    showlegend=True,
    geo=dict(
        landcolor='rgba(194, 178, 128, 0.7)'
    ),
    autosize=True,
    height=500,
    paper_bgcolor='rgba(233,233,233,0)',
    font_color='white',
    font_size=17
)

fig3.update_geos(
    showocean=True, oceancolor='rgba(0,71,114, 0.7)'
)


# ----------------------------------------------------------------------------------
# Dados 4

# 5 Publicadoras que mais publicaram e não fabricam consoles
publicadoras_apenas = ['Electronic Arts', 'Activision',
                       'Namco Bandai Games', 'Ubisoft', 'Konami Digital Entertainment']

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

        elif linha[5] == 'Electronic Arts' and linha[3] == float(i):
            ea_ += linha[10]

        elif linha[5] == 'Activision' and linha[3] == float(i):
            activision_ += linha[10]

        elif linha[5] == 'Take-Two Interactive' and linha[3] == float(i):
            take_two_ += linha[10]

        elif linha[5] == 'Namco Bandai Games' and linha[3] == float(i):
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
    fig4.add_trace(go.Scatter(
        x=anos_4, y=publicadoras_4[i - 1], mode='lines+markers', name=publicadoras_apenas[i - 1]))

fig4.update_traces(hoverinfo='name+y+x')

fig4.update_layout(title='Vendas por Editoras a Cada 5 Anos',
                   hovermode='x unified',
                   height=600,
                   width=856,
                   paper_bgcolor='rgba(233,233,233,0)',
                   plot_bgcolor='rgba(20,20,20,0.3)',
                   font_color='white',
                   font_size=17,
                   hoverlabel=dict(bgcolor='rgb(0,0,0)')
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
data = dict(
    consoles=['Plataforma', 'Sony', 'Microsoft', 'PC', 'Nintendo', 'Atari', 'SNK', 'PlayStation 3', 'Computador', 'PlayStation 4',
              'NES', 'PlayStation 2', 'Xbox 360', 'Nintendo 64', 'Xbox One', 'PSP', 'GameBoy', 'Atari2600', 'Nintendo Wii', 'NeoGeo'],
    empresas=['', 'Plataforma', 'Plataforma', 'Plataforma', 'Plataforma', 'Plataforma', 'Plataforma', 'Sony', 'PC',
              'Sony', 'Nintendo', 'Sony', 'Microsoft', 'Nintendo', 'Microsoft', 'Sony', 'Nintendo', 'Atari', 'Nintendo', 'SNK'],
    vendas=[plataforma, sony, microsoft, computador, nintendo, atari, snk, ps3, computador, ps4, nes, ps2, x360, n64, xone, psp, gb, atari, wii, ng])


# Gráfico 5
fig5 = px.sunburst(
    data,
    names='consoles',
    parents='empresas',
    values='vendas',
    title='Vendas por Plataformas das 5 Maiores Empresas'

)

fig5.update_layout(
    height=800,
    paper_bgcolor='rgba(233,233,233,0)',
    plot_bgcolor='rgba(20,20,20,0.3)',
    font_color='white',
    font_size=17
)

"""
Dash

Ideia geral:

HTML = esqueleto da página
CSS = beleza, estilo da página

Dividimos o uso do CSS em dois arquivos, nesse mesmo e no styles.css
Os estilos definidos nesse arquivo são os que serão alterados a partir da ação do botão, 
enquanto que os do arquivo styles.css são estilos mais fixos

Para referenciar um componente para poder alterar seu estilo com o CSS,
devemos dar um nome para o componente, por meio da propriedade "className".
Exemplo: "antes_style" logo abaixo é o className de html.Main lá em baixo,
logo após as divs com as nossas caras.

As propriedades do CSS são bem intuitivas, por exemplo, magin-top é a distância da div até a próxima div,
caso não entenda alguma das propriedades, é bom pesquisar.

O Dash é como se fosse um servidor local, que organiza os gráficos e estilos num layout, simulando um HTML & CSS,
o nosso Dash vai rodar na variável "app".

Basicamente, divs são divisórias, e podemos colocar várias divs dentro das outras para ir criando o layout,
uma ou mais divs dentro de outra podem ser chamadas de "children", pois teríamos uma div principal e divs filhas,

O botão recebe uma propriedade "n_clicks", que são quantas vezes esse botão foi clicado. Para que o programa faça 
ações com esses números de clicks, importamos lá em cima o "Input" e o "Output".
Input: tudo que o usuário envia para o servidor
Output: tudo que o servidor devolve para o usuário

Exemplo do primeiro gráfico, que serve para os outros Inputs e Outputs (IO):

@app.callback(
    Output('graph1', 'figure'),
    [Input('drop1', 'value')]
)
def update_graph_1(drop1):

O app.callback vai ler os IO da seguinte forma:

No input, ele vai pegar o "value" do ID da div, que no caso se chama drop1, por ser do dropdown.
Ou seja, ele vai ler qual valor está selecionado no dropdown.

No output, ele irá até a div com ID de "graph1" e vai alterar a propriedade "figure", que é a que renderiza os gráficos

Entre as ações de IO, ele executará o que está escrito após a função escrita depois de fechar os parenteses,
que no caso denominamos "update_graph_1", que recebe o valor de drop1.

No caso do exemplo, ele formará um gráfico novo, mas nos outros app.callback ele irá ficar alterando os estilos, que criamos logo abaixo

Como estudar para entender o que tá rolando em tudo:
Dar uma lida geral na parte do HTML, prestando atenção nas className e nos IDs, e ir comparando com os stlyes
Ler todos os app.callback, exercitando a parada lá de ler o quê da onde e retorna o quê aonde
Entender o que cada função depois do app.callback faz.


"""

antes_style = {
    'opacity': 0
}

depois_style = {
    'opacity': 1,
    'transition': 'opacity 3s ease-in-out'
}

button_style_antes = {
    'display': 'block',

}

button_style_durante = {
    'margin-top': '60vh',
    'height': 100,
    'width': 250,
    'transition': 'margin 0.5s ease-in-out, height 0.5s ease-in-out, width 0.5s ease-in-out',
    'z-index': 100
}

button_style_depois = {
    'display': 'none'
}

fonte_antes = {
    'font-size': 50,
}

fonte_depois = {
    'font-size': 40,
    'margin-top': '5vh',
    'transition': 'font-size 2s ease-in-out, margin-top 2s ease-in-out',
}

video_antes = {
    'background': 'url(./assets/background2.gif)',
    'height': '100vh',
    'background-position': 'center',
    'background-size': 'cover'
}

video_durante = {
    'background': 'url(./assets/background.gif)',
    'min-height': '100%',
    'background-position': 'center center',
    'background-size': 'cover',
    'width': '100%'
}

video_depois = {
    'height': 'auto',
    'min-height': '100%',
    'width': 'auto',
    'background-position': 'center',
    'background-size': 'cover',
    'background': 'url(./assets/wallpaper2.png) no-repeat',
    'background-attachment': 'fixed',
    'transition': 'background 3s ease-in-out'
}

grupo_antes = {
    'opacity': 0,
}

grupo_durante = {
    'opacity': 1,
    'margin-top': '-60vh',
    'transition': 'opacity 3s ease-in-out',
}

grupo_depois = {
    'opacity': 0,
    'height': 100,
    'margin-top': -50,
    'z-index': -2,
    'transition': 'height 2s ease-in-out'
}

# Inicializar o Dash na variável app
app = dash.Dash(__name__,
                title='Vendas de Jogos'
                )

# Estilizar o Dash
# Layout do Dash, sempre que quiser fazer o gráfico aparecer, colocar aqui
app.layout = html.Div(
    className='div-principal', id='video', style=video_antes,
    children=[
        html.Br(),
        html.Div(className='cabecalho', id='titulo', style=fonte_antes,
                 children=[
                     html.H1('GRUPO 4 - VENDAS DE JOGOS'),
                     html.H5('(Dados em milhões de unidades)'),
                     html.Button(id='btn', className='button', children=['PRESS TO START'],
                                 n_clicks=0, style=button_style_antes),
                     html.Div(className='grupo', id='fotos', style=grupo_antes, children=[
                         html.Div(className='primeira_fila', children=[

                             html.Img(src='./assets/brunao.png',
                                      style={'height': '230px'}),
                             html.Div(className='nickname_1', children=[
                                 'Bruno', html.Br(), '211031646']),

                             html.Img(src='./assets/filipao.png',
                                      style={'height': '240px'}),
                             html.Div(className='nickname_1', children=[
                                 'Filipe', html.Br(), '211030747']),

                             html.Img(src='./assets/geovanao.png',
                                      style={'height': '230px'}),
                             html.Div(className='nickname_1', children=[
                                 'Geovane', html.Br(), '211031708']),

                             html.Img(src='./assets/samucao.png',
                                      style={'height': '230px'}),
                             html.Div(className='nickname_1', children=[
                                 'Samuel', html.Br(), '211031495']),

                             html.Img(src='./assets/patrickao.png',
                                      style={'height': '260px'}),
                             html.Div(className='nickname_1', children=[
                                 'Patrick', html.Br(), '211030620']),
                         ]),
                         html.Br(),
                         html.Div(style={'font-size': 40}, className='segunda_fila', children=[
                             html.Div(children=[
                                 html.Div(className='nickname_1', children=[
                                     'Pedro', html.Br(), '211031468']),
                                 html.Img(src='./assets/pedrao.png',
                                          style={'height': '230px'}),
                             ]),
                             html.Div(children=[
                                 html.Div(className='nickname_1', children=[
                                     'Teodoro', html.Br(), '150149328 ']),
                                 html.Img(src='./assets/teodorao.png',
                                          style={'height': '230px'}),
                             ]),
                             html.Div(children=[
                                 html.Div(className='nickname_1', children=[
                                     'Gustavo Kenzo / ', 'Gustavo Henrique', html.Br(), '211029343 / ', '211030783']),
                                 html.Img(src='./assets/gustavoes.png',
                                          style={'height': '240px'}),
                             ]),
                             html.Div(children=[
                                 html.Div(className='nickname_1', children=[
                                     'Mateus', html.Br(), '202006484']),
                                 html.Img(src='./assets/mateusao.png',
                                          style={'height': '230px'}),
                             ]),
                             html.Div(children=[
                                 html.Div(className='nickname_1', children=[
                                     'Nicolas', html.Br(), '190098244']),
                                 html.Img(src='./assets/nicolao.png',
                                          style={'height': '230px'}),
                             ]),
                         ]),
                     ])
                 ]
                 ),

        html.Main(id='graphs', className='graficos',  style=antes_style,
                  children=[
                      html.Div(className='graficos_1', children=[
                          html.Div(
                              className='graph-1',
                              children=[
                                  html.Br(),
                                  dcc.Dropdown(id='drop1', className='dropdown',
                                               options=[{'label': str(j), 'value': j}
                                                        for j in order],
                                               value='Cronológico'),
                                  dcc.Graph(id='graph1')
                              ]
                          ),
                          html.Div(
                              id='graph-3', className='graph-3',
                              children=[
                                  dcc.Graph(figure=fig3)
                              ]
                          )
                      ]),

                      html.Div(className='graficos_2', children=[
                          html.Div(
                              id='graph-2', className='graph-2',
                              children=[
                                  dcc.Graph(figure=fig2)
                              ]
                          ),
                          html.Div(
                              id='graph-4',
                              children=[
                                  dcc.Graph(figure=fig4)
                              ]
                          )]),

                      html.Div(
                          id='graph-5',
                          children=[
                              dcc.Graph(figure=fig5)
                          ]
                      )
                  ]
                  )
    ]
)


@app.callback(
    Output('graph1', 'figure'),
    [Input('drop1', 'value')]
)
def update_graph_1(drop1):
    ordem = anos_filtro
    ordem_anos = todos
    vendas_anos_crescente = []
    vendas_anos_decrescente = []

    if drop1 == 'Crescente':
        ordem = sorted(ordem)

        for i in range(len(todos)):
            for j in range(len(anos_filtro)):
                if ordem[i] == anos_filtro[j]:
                    if todos[j] in vendas_anos_crescente:
                        continue
                    else:
                        vendas_anos_crescente.append(str(todos[j]))
                        break

        ordem_anos = vendas_anos_crescente

    elif drop1 == 'Decrescente':
        ordem = sorted(anos_filtro, reverse=True)

        for i in range(len(todos)):
            for j in range(len(anos_filtro)):
                if ordem[i] == anos_filtro[j]:
                    if todos[j] in vendas_anos_decrescente:
                        continue
                    else:
                        vendas_anos_decrescente.append(str(todos[j]))
                        break

        ordem_anos = vendas_anos_decrescente

    elif drop1 == 'Cronológico':
        ordem = anos_filtro
        ordem_anos = todos

    fig1 = px.bar(x=ordem_anos, y=ordem)

    fig1.update_layout(
        title='Vendas Globais por Ano',
        xaxis={'title': 'Anos'},
        yaxis={'title': 'Vendas'},
        height=500,
        paper_bgcolor='rgba(233,233,233,0)',
        plot_bgcolor='rgba(20,20,20,0.3)',
        font_color='white',
        font_size=17
    )

    fig1.update_traces(
        hovertemplate='Vendas: %{y} <br> Ano: %{x}'
    )

    return fig1


@app.callback(
    Output('graphs', 'style'),
    [Input('btn', 'n_clicks')]
)
def start_button(n_clicks):
    if n_clicks >= 2:
        return depois_style
    else:
        return antes_style


@app.callback(
    Output('btn', 'style'),
    [Input('btn', 'n_clicks')]
)
def sumir_botao(n_clicks):
    if n_clicks == 1:
        return button_style_durante

    elif n_clicks > 1:
        return button_style_depois

    else:
        return button_style_antes


@app.callback(
    Output('titulo', 'style'),
    [Input('btn', 'n_clicks')]
)
def mudar_fonte(n_clicks):
    if n_clicks >= 2:
        return fonte_depois
    else:
        return fonte_antes


@app.callback(
    Output('video', 'style'),
    [Input('btn', 'n_clicks')]
)
def mudar_video(n_clicks):
    if n_clicks == 1:
        return video_durante

    elif n_clicks > 1:
        return video_depois

    else:
        return video_antes


@app.callback(
    Output('fotos', 'style'),
    [Input('btn', 'n_clicks')],
)
def mudar_fotos(n_clicks):
    if n_clicks == 1:
        return grupo_durante

    elif n_clicks > 1:
        return grupo_depois

    else:
        return grupo_antes


# Rodar o Dash
# Para ficar mais dinâmico, basta deixar o código rodando apertar Ctrl + S para salvar,
# O Dash vai atualizar sozinho a cada 5 segundos +-, ou vc pode só clicar em reload mesmo
if __name__ == "__main__":
    app.run_server(debug=True)
