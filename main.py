# Importando bibliotecas
import dualsimplex as ds

A, b, c, tipo_problema, sinais_variaveis, sinal_restricao = ds.ler_arquivo_entrada('test.txt')

# Forma padrão
A, b, c, tipo_variavel = ds.transformar_padrao(A, b, c, tipo_problema, sinais_variaveis, sinal_restricao)

ds.imprimir_forma_padrao(A, b, c, tipo_variavel)

print('\n'+ '----------------------------------' + '\n')

# Primeira fase
A_fase1, c_fase1, tipo_variavel_fase1= ds.cria_primeira_fase(A, c, tipo_variavel)

ds.imprimir_primeira_fase(A_fase1, b, c_fase1, tipo_variavel_fase1)
