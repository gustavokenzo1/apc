todos = [1980, 1981, 1982, 1983, 1984]
ordem = [10, 2, 4, 50, 19]

ordem_crescente = sorted(ordem)
todos_anos_vendas_crescente = []

for i in range(len(todos)):
    for j in range(len(ordem)):
        if ordem_crescente[i] == ordem[j]:
            todos_anos_vendas_crescente.append(todos[j])

print(todos_anos_vendas_crescente)
