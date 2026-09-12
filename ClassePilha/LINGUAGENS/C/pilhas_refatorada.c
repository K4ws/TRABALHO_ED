#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

// Enumeração para controle rígido do tipo de dado da pilha
typedef enum {
    TIPO_INT,
    TIPO_FLOAT,
    TIPO_CHAR
} TipoDado;

// Union para permitir armazenamento heterogêneo na estrutura física, porém restrito pela pilha
typedef union {
    int v_int;
    float v_float;
    char v_char;
} Elemento;

// Estrutura principal da Pilha
typedef struct {
    Elemento* dados;
    size_t capacidade;
    size_t quantidade;
    TipoDado tipo;
} Pilha;

// Função para criar a pilha com alocação estática inicial do bloco completo de memória
Pilha* criar_pilha(size_t capacidade, TipoDado tipo) {
    if (capacidade == 0) {
        fprintf(stderr, "Erro: A capacidade deve ser maior que zero.\n");
        exit(EXIT_FAILURE);
    }

    Pilha* p = (Pilha*) malloc(sizeof(Pilha));
    if (!p) {
        fprintf(stderr, "Erro de alocacao de memoria para a estrutura.\n");
        exit(EXIT_FAILURE);
    }

    p->capacidade = capacidade;
    p->quantidade = 0;
    p->tipo = tipo;

    // Alocação estática prévia do bloco contíguo total
    p->dados = (Elemento*) malloc(capacidade * sizeof(Elemento));
    if (!p->dados) {
        fprintf(stderr, "Erro de alocacao de memoria para os dados.\n");
        free(p);
        exit(EXIT_FAILURE);
    }

    return p;
}

void destruir_pilha(Pilha* p) {
    if (p) {
        if (p->dados) free(p->dados);
        free(p);
    }
}

bool pilha_esta_vazia(Pilha* p) {
    return p->quantidade == 0;
}

bool pilha_esta_cheia(Pilha* p) {
    return p->quantidade == p->capacidade;
}

size_t tamanho(Pilha* p) {
    return p->quantidade;
}

bool empilha(Pilha* p, Elemento dado) {
    if (pilha_esta_cheia(p)) {
        fprintf(stderr, "PilhaCheiaErro: A pilha esta cheia.\n");
        return false;
    }

    // Insere no topo e incrementa o ponteiro de quantidade
    p->dados[p->quantidade] = dado;
    p->quantidade++;
    return true;
}

bool desempilha(Pilha* p, Elemento* valor_out) {
    if (pilha_esta_vazia(p)) {
        fprintf(stderr, "PilhaVaziaErro: A pilha esta vazia.\n");
        return false;
    }

    p->quantidade--;
    *valor_out = p->dados[p->quantidade];
    return true;
}

bool troca(Pilha* p) {
    if (p->quantidade < 2) {
        fprintf(stderr, "PilhaVaziaErro: Eh necessario ter pelo menos 2 elementos para trocar.\n");
        return false;
    }

    size_t topo = p->quantidade - 1;
    size_t abaixo = p->quantidade - 2;

    Elemento temp = p->dados[topo];
    p->dados[topo] = p->dados[abaixo];
    p->dados[abaixo] = temp;
    return true;
}

// --- BATERIA DE TESTES AUTOMATIZADOS E ESTRESSE ---
int main() {
    printf("==================================================\n");
    printf("     INICIANDO BATERIA DE TESTES DA PILHA (C)     \n");
    printf("==================================================\n\n");

    // 1. Teste com Inteiros
    printf("[TESTE 1] Operacoes Basicas com Inteiros...\n");
    Pilha* pInt = criar_pilha(3, TIPO_INT);
    assert(pilha_esta_vazia(pInt) == true);

    Elemento e1 = {.v_int = 10};
    Elemento e2 = {.v_int = 20};
    Elemento e3 = {.v_int = 30};

    empilha(pInt, e1);
    empilha(pInt, e2);
    empilha(pInt, e3);

    assert(tamanho(pInt) == 3);
    assert(pilha_esta_cheia(pInt) == true);

    Elemento removido;
    desempilha(pInt, &removido);
    assert(removido.v_int == 30);
    printf("  ✓ Elemento desempilhado: %d\n", removido.v_int);

    // Teste da Troca
    troca(pInt);
    desempilha(pInt, &removido);
    assert(removido.v_int == 10);
    printf("  ✓ Elemento apos troca desempilhado: %d\n", removido.v_int);
    printf("  [PASS] Teste 1 concluido com sucesso!\n\n");

    destruir_pilha(pInt);

    // 2. Cenário de Estresse: Pilha Cheia (Overflow)
    printf("[TESTE 2] Cenario de Estresse: Pilha Cheia (Overflow)...\n");
    Pilha* pCheia = criar_pilha(2, TIPO_INT);
    empilha(pCheia, e1);
    empilha(pCheia, e2);

    bool ok = empilha(pCheia, e3);
    assert(ok == false);
    printf("  ✓ Bloqueio de insercao em pilha cheia confirmado.\n");
    printf("  [PASS] Teste 2 (Overflow) concluido com sucesso!\n\n");

    destruir_pilha(pCheia);

    // 3. Cenário de Estresse: Pilha Vazia (Underflow)
    printf("[TESTE 3] Cenario de Estresse: Pilha Vazia (Underflow)...\n");
    Pilha* pVazia = criar_pilha(3, TIPO_INT);

    ok = desempilha(pVazia, &removido);
    assert(ok == false);

    ok = troca(pVazia);
    assert(ok == false);
    printf("  ✓ Bloqueio de remocao e troca em pilha vazia confirmado.\n");
    printf("  [PASS] Teste 3 (Underflow) concluido com sucesso!\n\n");

    destruir_pilha(pVazia);

    // 4. Teste com Caractere (char)
    printf("[TESTE 4] Operacoes com Caractere (char)...\n");
    Pilha* pChar = criar_pilha(2, TIPO_CHAR);
    Elemento c1 = {.v_char = 'A'};
    Elemento c2 = {.v_char = 'B'};

    empilha(pChar, c1);
    empilha(pChar, c2);

    desempilha(pChar, &removido);
    assert(removido.v_char == 'B');
    printf("  ✓ Caractere desempilhado corretamente: %c\n", removido.v_char);
    printf("  [PASS] Teste 4 (char) concluido com sucesso!\n\n");

    destruir_pilha(pChar);

    printf("==================================================\n");
    printf("   TODOS OS TESTES EM C FORAM EXECUTADOS COM SUCESSO! \n");
    printf("==================================================\n");

    return 0;
}