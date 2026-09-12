Log de Iteração e Prompts Iniciais — Linguagem C

Prompt Enviado ao Modelo de IA:

Desenvolver uma estrutura de dados Pilha em Linguagem C que atenda aos princípios de Programação Orientada a Objetos/TAD. A pilha deve utilizar um array para armazenamento em memória contígua com capacidade máxima predefinida. A implementação deve suportar tipos básicos e conter as funções empilha, desempilha, pilha\_esta\_vazia, pilha\_esta\_cheia, troca e tamanho, além de tratar cenários de erro como pilha cheia e pilha vazia.

Código Bruto Gerado pela IA (Versão Inicial Ineficiente):

#include <stdio.h>

#include <stdlib.h>

typedef struct {

int\* dados;

size\_t capacidade;

size\_t quantidade;

} Pilha;

Pilha\* criar\_pilha(size\_t capacidade) {

Pilha\* p = (Pilha\*) malloc(sizeof(Pilha));

p->capacidade = capacidade;

p->quantidade = 0;

p->dados = NULL;

return p;

}

void empilha(Pilha\* p, int dado) {

if (p->quantidade < p->capacidade) {

p->dados = (int\*) realloc(p->dados, (p->quantidade + 1) \* sizeof(int));

p->dados[p->quantidade++] = dado;

}

}

int desempilha(Pilha\* p) {

if (p->quantidade > 0) {

p->quantidade--;

return p->dados[p->quantidade];

}

return -1;

}
