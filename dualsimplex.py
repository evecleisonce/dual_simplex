# Definindo funções importantes para a implementação do algoritmo dual simplex
# Autor: Lucas José Lemos Braz

import numpy as np
import pandas as pd
import math

# Função para ler o arquivo de entrada e retornar a matrix A e os vetores b e c, tipo de prob e número de variáveis e
# restrições Primeira linha do arquivo: número de variáveis N e número de restrições M Segunda linha do arquivo: 0 se
# for minimização e 1 se for maximização Terceira linha: N caracteres do vetor c M linhas seguintes: matriz A,
# onde o primeiro caractere é o tipo de restrição (0 para <=, 1 para >= e 2 para =), seguido de N caracteres Linha
# Seguinte: M caracteres do vetor b Linha Seguinte: N caracteres, onde 0 se for não negativas e 1 se for livres,
# 2 se for negativas.

def ler_arquivo_entrada(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()


    # Extrair o número de variáveis (N) e número de restrições (M)
    N, M = map(int, linhas[0].strip().split())

    # Extrair o tipo de problema (0 para minimização, 1 para maximização)
    tipo_problema = int(linhas[1].strip())

    # Extrair o vetor c
    c = list(map(float, linhas[2].strip().split()))

    # Extrair a matriz A e o vetor de sinais das restrições
    sinal_restricao = []
    A = []
    for linha in linhas[3:3+M]:
        A.append(list(map(float, linha[1:].strip().split())))
        # Pega a primeira coluna da matriz A, de cada linha, e salva em sinal_restricao
        sinal_restricao.append(int(linha[0]))

    # Extrair o vetor b
    b = list(map(float, linhas[3+M].strip().split()))

    # Extrair a lista de sinais das variáveis (0 para não negativas, 1 para livres, 2 para negativas)
    sinais_variaveis = list(map(int, linhas[4+M].strip().split()))

    return A, b, c, tipo_problema, sinais_variaveis, sinal_restricao


# Função para converter o problema de maximização para minimização
def converter_max_min(c, tipo_problema):
    if tipo_problema == 1:
        c_convert = [-x for x in c]
        return c_convert
    else:
        return c

# Função para remover inequaçao seguindo a regra de sinal_restricao
# 0 para <=, 1 para >= e 2 para =
def remover_inequacao(A, c, sinal_restricao, sinais_variaveis):
    A_convert = []
    tipo_variavel = []
    c_convert = c.copy()
    sinais_var_convt= sinais_variaveis.copy()
    tipo_variavel = (np.zeros_like(sinais_variaveis)).tolist()

    for i in range(len(sinal_restricao)):
    # É iqualdade então mantem.
        if sinal_restricao[i] == 2:
            if i != len(A)-1:
                A_convert.append(A[i])
                c_convert.append(c[i])

        # É maior ou igual então adiciona uma variável de folga na linha e zeros nas outras.
        # Adiciona 0 no vetor c
        elif sinal_restricao[i] == 1:
            A_convert.append(A[i])
            A_convert[i].append(1)
            c_convert.append(0)
            # Adiciona zero nas outras linhas
            sinais_var_convt.append(0)
            tipo_variavel.append('f')
            if i != len(A)-1:
                A_convert.append(A[i+1])
            for j in range(len(A)):
                if j != i:
                    A_convert[j].append(0)
        # É menor ou igual então adiciona uma variável de folga "negativa" na linha e zeros nas outras.
        # Adiciona 0 no vetor c
        elif sinal_restricao[i] == 0:
            A_convert.append(A[i])
            A_convert[i].append(-1)
            c_convert.append(0)

            sinais_var_convt.append(0)
            tipo_variavel.append('f')
            # Preciso verificar se está na ultima linha ou não, se não tiver pega a proxima e adiciona, se tiver, não faz nada
            if i != len(A)-1:
                A_convert.append(A[i+1])
            # Adiciona zero nas outras linhas
            for j in range(len(A)):
                if j != i:
                    A_convert[j].append(0)
    # Agora com a matriz convertida deixa
    return A, c_convert, sinais_var_convt, tipo_variavel

# Função para transformar as variáveis livres e negativas em não negativas
# 0 para não negativas, 1 para livres, 2 para negativas
# Caso seja nao negativa, so mantem;
# Caso seja negativa, multiplica a coluna da variavel por -1, inclusive a coluna referente ao vetor c;
# Caso seja livre, troca a variavel por duas variaveis nao negativas, uma positiva e outra negativa,
# e no vetor C substitui a variavel por duas variaveis, uma positiva e outra negativa;
# Levando em consideração que A é uma Matriz e c é um vetor.
def transformar_variaveis_nao_negativas(A, b, c, sinais_variaveis):
    A = np.array(A)
    c = np.array(c)
    sinais_variaveis = np.array(sinais_variaveis)

    num_variaveis = A.shape[1]
    num_restricoes = A.shape[0]

    # Transformar variáveis negativas
    for i in range(num_variaveis):
        if sinais_variaveis[i] == 2:  # Variável negativa
            A[:, i] *= -1
            c[i] *= -1

    # Transformar variáveis livres
    A_transformed = []
    b_transformed = []
    c_transformed = []

    for i in range(num_variaveis):
        if sinais_variaveis[i] == 1:  # Variável livre
            # Introduzir duas variáveis não negativas
            A_transformed.append(A[:, i])
            A_transformed.append(-A[:, i])
            b_transformed.append(b)
            b_transformed.append(-b)
            c_transformed.append(c[i])
            c_transformed.append(-c[i])
        else:  # Variável não negativa
            A_transformed.append(A[:, i])
            b_transformed.append(b)
            c_transformed.append(c[i])

    A_transformed = np.array(A_transformed).T
    b_transformed = np.array(b_transformed[0])
    c_transformed = np.array(c_transformed)

    return A_transformed.tolist(), b_transformed.tolist(), c_transformed.tolist()

# Função para sinal negativo do vetor b.
# Caso seja negativo, multiplica a o elemento do vetor por -1, e multiplica a linha da matriz por A -1.
def remover_negativos_b(A, b):
    for i in range(len(b)):
        if b[i] < 0:
            b[i] = b[i]*(-1)
            A[i] = [ele * (-1) for ele in A[i]]
    return A, b


# Finalmente transoforma na forma padrão
def transformar_padrao(A, b, c, tipo_problema, sinais_variaveis, sinal_restricao):
    # Converter problema de maximização para minimização
    c = converter_max_min(c, tipo_problema)

    # Remover inequações
    A, c, sinais_variaveis, tipo_variavel = remover_inequacao(A, c, sinal_restricao, sinais_variaveis)

    # Transformar variáveis livres e negativas em não negativas
    A, b, c = transformar_variaveis_nao_negativas(A, b, c, sinais_variaveis)

    # Remover negativos do vetor b
    A, b = remover_negativos_b(A, b)

    return A, b, c, tipo_variavel

def imprimir_forma_padrao(A, b, c, tipo_variavel):
    num_variaveis = len(c)
    num_restricoes = len(b)

    # Imprimir a função objetivo
    objetivo = ""
    if c[0] >= 0 and tipo_variavel[0] == 0:
        objetivo += " {}x{}".format(c[0], 1)
    elif c[0] < 0 and tipo_variavel[0] == 0:
        objetivo += " -{}x{}".format(-c[0], 1)
    for i in range(1,num_variaveis):
        if c[i] >= 0:
            objetivo += " +{}x{}".format(c[i], i+1)
        else:
            objetivo += " -{}x{}".format(-c[i], i+1)
    print("Min ", objetivo)

    # Imprimir as restrições
    print("s.t:")
    for i in range(num_restricoes):
        restricao = ""
        if A[i][0] > 0 and tipo_variavel[0] == 0:
            restricao += " {}x{}".format(A[i][0], 1)
        elif A[i][0] <= 0 and tipo_variavel[0] == 0:
            restricao += " -{}x{}".format(-A[i][0], 1)
        elif A[i][0] > 0 and tipo_variavel[0] == 'f':
            restricao += " {}f{}1".format(A[i][0], 1)
        elif A[i][0] <= 0 and tipo_variavel[0] == 'f':
            restricao += " -{}f{}1".format(-A[i][0], 1)

        f = 1
        for j in range(1,num_variaveis):
            if A[i][j] > 0 and tipo_variavel[j] == 0:
                restricao += " +{}x{}".format(A[i][j], j+1)
            elif A[i][j] <= 0 and tipo_variavel[j] == 0:
                restricao += " -{}x{}".format(-A[i][j], j+1)
            elif A[i][j] > 0 and tipo_variavel[j] == 'f':
                restricao += " +{}f{}".format(A[i][j], f)
                f += 1
            elif A[i][j] <= 0 and tipo_variavel[j] == 'f':
                restricao += " -{}f{}".format(-A[i][j], f)
                f += 1
        restricao += " = {}".format(b[i])
        print('\t'+restricao)

    # Imprimir as condições de não negatividade
    for i in range(num_variaveis):
        print("\t\t"+"x{},".format(i+1), end="")

    # Imprimindo variaveis de folga
    print(" >= 0")


# Tenho a forma padrão, agora preciso criar a primeira fase
# A primeira fase é criada adicionando uma variável de 'y' para cada restrição
# A função objetivo é minimizar a soma de todas as variáveis 'y' que tem peso 1

# Eu tenho que adiconar tipo_variavel = 'y' para cada variável 'y' adicionada
# Quando for imprimir o primeira fase, eu tenho que imprimir as variáveis 'y' também
# Depois de resolver a primeira fase, eu tenho que se a solução ótima é 0, se for,
# eu posso remover as variáveis 'y' e resolver o problema original

# É importante manter em mente o vetor que as variaveis da primeira fase, para ver se tem y na base.



# FUnção para criar a primeira fase
def cria_primeira_fase(A, c,tipo_variavel):
    A = np.array(A)
    c = np.array(c)

    num_variaveis = len(c)
    num_restricoes = len(A)

    # Criando a matriz A da primeira fase
    # Adiciona uma matrix identidade de tamanho num_restricoes
    A_primeira_fase = np.concatenate((A, np.identity(num_restricoes)), axis=1)

    # Criando o vetor c da primeira fase
    # Um vetor de zeros de tamanho num_varivaeis, e um vetor de 1 de tamanho num_restricoes
    c_primeira_fase = np.concatenate((np.zeros(num_variaveis), np.ones(num_restricoes)), axis=0)

    # Manter em mente o tipo de variável
    tipo_variavel_primeira_fase = tipo_variavel + ['y']*num_restricoes

    return A_primeira_fase.tolist(), c_primeira_fase.tolist(), tipo_variavel_primeira_fase


# Função para imprimir a primeira fase
def imprimir_primeira_fase(A, b, c, tipo_variavel):
    # Imprimir a função objetivo que é minimizar a soma de todas as variáveis 'y'
    num_variaveis = len(c)
    num_restricoes = len(b)

    objetivo = ""
    for i in range(num_variaveis):
        if tipo_variavel[i] == 'y':
            objetivo += " +{}y{}".format(c[i], i+1)
        else:
            objetivo += " "
    print("Min ", objetivo)

    # Imprimir as restrições
    # Mantendo em mente que se tipo_variavel for 0 é x, se for 'f' é folga e se for 'y' é y
    # Imprimir as restrições
    print("s.t:")
    for i in range(num_restricoes):
        restricao = ""
        if A[i][0] > 0 and tipo_variavel[0] == 0:
            restricao += " {}x{}".format(A[i][0], 1)
        elif A[i][0] <= 0 and tipo_variavel[0] == 0:
            restricao += " -{}x{}".format(-A[i][0], 1)
        elif A[i][0] > 0 and tipo_variavel[0] == 'f':
            restricao += " {}f{}1".format(A[i][0], 1)
        elif A[i][0] <= 0 and tipo_variavel[0] == 'f':
            restricao += " -{}f{}1".format(-A[i][0], 1)

        f = 1
        y = 1
        for j in range(1, num_variaveis):
            if A[i][j] > 0 and tipo_variavel[j] == 0:
                restricao += " +{}x{}".format(A[i][j], j + 1)
            elif A[i][j] <= 0 and tipo_variavel[j] == 0:
                restricao += " -{}x{}".format(-A[i][j], j + 1)
            elif A[i][j] > 0 and tipo_variavel[j] == 'f':
                restricao += " +{}f{}".format(A[i][j], f)
                f += 1
            elif A[i][j] <= 0 and tipo_variavel[j] == 'f':
                restricao += " -{}f{}".format(-A[i][j], f)
                f += 1
            elif A[i][j] > 0 and tipo_variavel[j] == 'y':
                restricao += " +{}y{}".format(A[i][j], y)
                y += 1
            elif A[i][j] <= 0 and tipo_variavel[j] == 'y':
                restricao += " -{}y{}".format(-A[i][j], y)
                y += 1
        restricao += " = {}".format(b[i])
        print('\t' + restricao)

    # Imprimir as condições de não negatividade
    print("\t\t", end="")
    for i in range(num_variaveis):
        print(" "+"x{},".format(i+1), end="")
    for i in range(num_restricoes):
        print(" "+"y{},".format(i+1), end="")
    print(" >= 0")

