#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Exceções/Erros simulados via códigos de status
typedef enum {
    SUCESSO = 0,
    ERRO_PILHA_CHEIA = 1,
    ERRO_PILHA_VAZIA = 2,
    ERRO_TIPO_INVALIDO = 3
} StatusPilha;

// Estrutura Inicial (com falhas de alocação)
typedef struct {
    int* dados;         // FALHA: Aceita apenas int e não usa union/enum para tipagem flexível
    size_t capacidade;  // Capacidade informada
    size_t quantidade;  // Quantidade atual
} PilhaInicial;

PilhaInicial* criar_pilha_inicial(size_t capacidade) {
    PilhaInicial* p = (PilhaInicial*) malloc(sizeof(PilhaInicial));
    p->capacidade = capacidade;
    p->quantidade = 0;
    p->dados = NULL; // FALHA: Ponteiro nulo, não aloca a capacidade total no construtor
    return p;
}

void destruir_pilha_inicial(PilhaInicial* p) {
    if (p) {
        if (p->dados) free(p->dados);
        free(p);
    }
}

bool pilha_esta_vazia_inicial(PilhaInicial* p) {
    return p->quantidade == 0;
}

bool pilha_esta_cheia_inicial(PilhaInicial* p) {
    return p->quantidade == p->capacidade;
}

size_t tamanho_inicial(PilhaInicial* p) {
    return p->quantidade;
}

StatusPilha empilha_inicial(PilhaInicial* p, int dado) {
    if (pilha_esta_cheia_inicial(p)) {
        printf("PilhaCheiaErro: A pilha esta cheia.\n");
        return ERRO_PILHA_CHEIA;
    }
    // FALHA: Realocação progressiva de memória a cada inserção
    p->dados = (int*) realloc(p->dados, (p->quantidade + 1) * sizeof(int));
    p->dados[p->quantidade] = dado;
    p->quantidade++;
    return SUCESSO;
}

StatusPilha desempilha_inicial(PilhaInicial* p, int* valor_out) {
    if (pilha_esta_vazia_inicial(p)) {
        printf("PilhaVaziaErro: A pilha esta vazia.\n");
        return ERRO_PILHA_VAZIA;
    }
    p->quantidade--;
    *valor_out = p->dados[p->quantidade];
    return SUCESSO;
}

void troca_inicial(PilhaInicial* p) {
    if (p->quantidade >= 2) {
        int temp = p->dados[p->quantidade - 1];
        p->dados[p->quantidade - 1] = p->dados[p->quantidade - 2];
        p->dados[p->quantidade - 2] = temp;
    }
}

// --- TESTE INICIAL EM C ---
int main() {
    printf("--- Executando Teste Inicial em Linguagem C ---\n");

    PilhaInicial* p = criar_pilha_inicial(3);

    empilha_inicial(p, 10);
    empilha_inicial(p, 20);
    empilha_inicial(p, 30);

    printf("Tamanho atual: %zu\n", tamanho_inicial(p));
    printf("Esta cheia?: %s\n", pilha_esta_cheia_inicial(p) ? "Sim" : "Nao");

    int valor_removido;
    desempilha_inicial(p, &valor_removido);
    printf("Elemento removido: %d\n", valor_removido);
    printf("Tamanho apos remocao: %zu\n", tamanho_inicial(p));

    destruir_pilha_inicial(p);
    return 0;
}