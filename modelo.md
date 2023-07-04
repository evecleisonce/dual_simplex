Suponha que tenhamos uma problema com m restrições e n variáveis. O arquivo terá o seguinte formato:

Na primeira linha teremos três inteiros positivos separados por um espaço simples. Ou seja, será "t m n", onde 
-- o primeiro valor se refere ao tipo do problema. Adotaremos 0 para minimização e 1 para maximização
-- o segundo valor se refere a quantidade de restrições do nosso problema
-- o terceiro valor se refere a quantidade de variáveis do nosso problema.

A segunda linha será referente a função objetivo e terá m valores do tipo decimal separadas por um espaço simples. Cada um desses valores se refere ao conficiente da variável de mesma posição. Ou seja, se seu problema possui variáveis x_1, ..., x_n então a i-ésima entrada dessa linha se refere ao coeficiente da função objetiva referente a i-ésima variável (Ver exemplo no final para maior clareza).

A partir da segunda linha teremos uma sequência de m pares de linhas referente as restrições. 
A primeira linha de cada par conterá um valor inteiro -1, 0 ou 1 referente ao tipo de restrição. Adotaremos -1 para restrição de menor igual, 0 para restrição de igual e 1 para restrição de maior ou igual. 
A segunda linha de cada par conterá uma sequência de n+1 valores decimais separados por espaço simples, onde cada entrada se refere ao coeficiente da variável daquela restrição e o último valor se refere ao valor a direita da desigualdade da restrição.

Por fim, o arquivo conterá uma sequência de n restrições referente as restrições de sinais das variáveis do seu problema. Cada restrição de sinal será formada por dois valores, um inteiro referente ao tipo de restrição (-1 se menor ou igual e 1 se maior ou igual) e um decimal referente ao valor de limitação. Caso a variável seja livre, a restrição terá apenas um valor coringa que adotaremos como sendo o 0.

Para padronização do trabalho, todas as variáveis do primal deverão ser chamadas de x e todas primal de u.

Exemplo.
O problema
```
max 2x1 + 3x2 + 4x3
s.a. x1 - 1.2x2 + 3x3 <= 4
     x1 + x2 + x3 >= 4
     x1 + 2x2 + x3 = 5
x1 >= 1
x2 <= 2
x3 livre 
```
terá modelo

````
1 3 3
2 3 4
-1
1 -1.2 3 4
1
1 1 1 4
0
1 2 1 5
1 1
-1 2
0
````