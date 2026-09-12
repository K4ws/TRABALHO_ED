```
Code Review Crítico — Linguagem C
```

```
A análise detalhada da solução inicial desenvolvida em C revelou falhas graves
de arquitetura de software, alocação de memória e descumprimento de requisitos
do projeto:
```

```
Realocação Dinâmica Indevida de Memória (Uso de realloc)
```

```
A versão inicial utilizou a função realloc() a cada chamada de empilhamento.
Essa abordagem ignora o requisito de capacidade estática fixa, pois o vetor
expande em tempo de execução no heap em vez de ser pré-alocado no construtor.
Além disso, realloc() introduz sobrecarga operacional de complexidade de tempo e
risco de fragmentação de memória.
```

```
Inicialização com Ponteiro Nulo e Risco de Leaks
```

```
A função criar_pilha_inicial() definia p->dados = NULL na instanciação. Delegar
a alocação de memória para as chamadas da função empilha() cria riscos de
vazamento de memória (memory leak) em caso de falhas de alocação no realloc(),
além de deixar a estrutura em estado inconsistente.
```

```
Ausência de Suporte a Outros Tipos Primitivos
```

```
O código foi escrito de forma rígida aceitando apenas o tipo int (int* dados).
Não foi implementada uma estrutura com union e enum para garantir a restrição de
tipo único por pilha e o suporte aos tipos float e char (caractere individual)
exigidos no enunciado.
```

```
Tratamento de Erros Frágil no Desempilhamento
```

```
O retorno de valores de erro baseava-se em retornos arbitrários ou mensagens de
texto via printf(). Sem um controle por ponteiro de status ou códigos de erro
estruturados, o programa não impede o retorno de lixo de memória em situações de
subflutuação (pilha vazia).
```

