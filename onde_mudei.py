# Função para imprimir a primeira fase
def imprimir_primeira_fase(A, b, c, tipo_variavel):
    # Imprimir a função objetivo que é minimizar a soma de todas as variáveis 'y'
    num_variaveis = len(c)
    num_restricoes = len(b)
    num_variaveis_y = num_variaveis - num_restricoes#numero de variáveis y
    
    objetivo = ""
    for i in range(num_variaveis):
        if tipo_variavel[i] == 'y':
            objetivo += " +{}y{}".format(c[i], i + 1 - num_variaveis_y)
        else:
            objetivo += " "
    print("Min ", objetivo)
