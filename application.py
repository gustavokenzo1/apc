# Importar leitor de csv
from csv import reader

# Abrir a base de dados e guardar na variável "arquivo_csv"
with open('vgsales.csv') as arquivo_csv:

    # Ler a base de dados e guardar na variável "leitor_csv"
    leitor_csv = reader(arquivo_csv)

    # Para cada linha da base de dados, printar, por exemplo, a coluna "Name", que é a coluna 1
    for linha in leitor_csv:
        print(linha[1])