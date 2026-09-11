"""Preenchimento de região por rotina recursiva.

A rotina recursiva "pura" (`_preencher`) é a especificada no enunciado: a
partir de uma posição, marca a célula e recorre para os quatro vizinhos.
Ela é executada dentro de uma thread dedicada, com pilha nativa maior e
limite de recursão do interpretador ajustado ao tamanho da matriz — sem
isso, regiões grandes e "abertas" (poucas bifurcações, muitas células
conectadas em sequência) estouram o limite padrão de recursão do Python
bem antes de esgotar a memória disponível. Veja CODE_REVIEW.md para a
motivação detalhada dessa decisão.
"""

import sys
import threading

from matriz_io import VIZINHANCA_4

TAMANHO_PILHA_NATIVA = 64 * 1024 * 1024  # 64 MiB de folga para recursões profundas


def _preencher(matriz, linha, coluna, n_linhas, n_colunas, novo, alvo, eventos):
    if not (0 <= linha < n_linhas and 0 <= coluna < n_colunas):
        return
    if matriz[linha][coluna] != alvo:
        return

    matriz[linha][coluna] = novo
    eventos.append((linha, coluna))

    for delta_linha, delta_coluna in VIZINHANCA_4:
        _preencher(
            matriz, linha + delta_linha, coluna + delta_coluna,
            n_linhas, n_colunas, novo, alvo, eventos,
        )


def preencher(matriz, linha, coluna, novo="0", alvo="1"):
    """Preenche, por recursão, a região de `alvo`s conectada a (linha, coluna).

    Altera `matriz` em memória e devolve a lista ordenada das posições
    preenchidas (na ordem em que a recursão as visitou), usada pelos
    reprodutores (texto ou interface gráfica) para repetir a evolução do
    algoritmo passo a passo.
    """
    n_linhas = len(matriz)
    n_colunas = len(matriz[0]) if n_linhas else 0
    eventos = []
    erro = []

    def executar_com_seguranca():
        limite_anterior = sys.getrecursionlimit()
        sys.setrecursionlimit(max(limite_anterior, n_linhas * n_colunas + 200))
        try:
            _preencher(matriz, linha, coluna, n_linhas, n_colunas, novo, alvo, eventos)
        except Exception as excecao:  # propagada para a thread principal abaixo
            erro.append(excecao)
        finally:
            sys.setrecursionlimit(limite_anterior)

    pilha_nativa_anterior = threading.stack_size()
    threading.stack_size(TAMANHO_PILHA_NATIVA)
    try:
        execucao = threading.Thread(target=executar_com_seguranca)
        execucao.start()
        execucao.join()
    finally:
        threading.stack_size(pilha_nativa_anterior)

    if erro:
        raise erro[0]
    return eventos
