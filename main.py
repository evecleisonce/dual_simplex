# Importando bibliotecas
import dualsimplex as ds
import numpy as np
A, b, c, tipo_problema, sinal_restricao, sinais_variaveis, valor_limite = ds.ler_arquivo_entrada('ex6_5.txt')

# Forma padrão
A, b, c, tipo_variavel = ds.transformar_padrao(A, b, c, tipo_problema, sinais_variaveis, sinal_restricao, valor_limite)

ds.imprimir_forma_padrao(A, b, c, tipo_variavel)

print('\n'+ '----------------------------------' + '\n')

# Primeira fase
A_fase1, c_fase1, tipo_variavel_fase1= ds.cria_primeira_fase(A, c, tipo_variavel)

ds.imprimir_primeira_fase(A_fase1, b, c_fase1, tipo_variavel_fase1)
B_inv, B, N, c_B, c_N, base_indices, org_B, org_N = ds.simplex_primeira_fase(A_fase1, b, c_fase1,tipo_variavel_fase1)


print('\n'+ '----------------------------------' + '\n')
A_aux, b_aux, c_aux, tipo_variavel, base_indices = ds.criar_problema_auxiliar(A_fase1, b, c, tipo_variavel_fase1, base_indices)

B_inv, B, N, c_B, c_N, base_indices = ds.simplex(A_aux, b_aux, c_aux, base_indices)


print('\n'+ '----------------------------------' + '\n')

