"""Testes de estresse: comparam as versões finais com as versões ingênuas
que motivaram a revisão (ver CODE_REVIEW.md e POST_MORTEM.md). As versões
ingênuas só existem aqui, para fins de comparação — não fazem parte da
solução entregue.
"""

import sys
import time

import pytest

import preenchimento_pilha
import preenchimento_recursivo
from pilha import Pilha


def _montar_sala(n_linhas, n_colunas):
    """Sala retangular vazia: bordas '0', interior '1' (lista de listas de caracteres)."""
    matriz = [list("0" * n_colunas)]
    for _ in range(n_linhas - 2):
        matriz.append(list("0" + "1" * (n_colunas - 2) + "0"))
    matriz.append(list("0" * n_colunas))
    return matriz


def _montar_sala_strings(n_linhas, n_colunas):
    """Mesma sala, mas como lista de strings (imutáveis) — usada só pela versão ingênua."""
    linhas = ["0" * n_colunas]
    linhas += ["0" + "1" * (n_colunas - 2) + "0" for _ in range(n_linhas - 2)]
    linhas.append("0" * n_colunas)
    return linhas


def _menor_tempo(funcao, repeticoes=3):
    """Executa `funcao` algumas vezes e devolve o menor tempo (reduz ruído de medição)."""
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao()
        tempos.append(time.perf_counter() - inicio)
    return min(tempos)


# ---------------------------------------------------------------------------
# Versão ingênua do preenchimento com pilha: duas Pilhas paralelas (linhas e
# colunas), empilhando os quatro vizinhos incondicionalmente e só validando
# ao desempilhar. Precisa de uma capacidade "estimada" por excesso, porque
# uma mesma célula pode ser empilhada várias vezes antes de ser marcada.
# ---------------------------------------------------------------------------
def _preencher_ingenuo_com_pilhas_paralelas(matriz, linha, coluna, novo="0", alvo="1"):
    n_linhas, n_colunas = len(matriz), len(matriz[0])
    capacidade_estimada = n_linhas * n_colunas * 4

    pilha_linhas = Pilha(capacidade_estimada, int)
    pilha_colunas = Pilha(capacidade_estimada, int)
    pilha_linhas.empilha(linha)
    pilha_colunas.empilha(coluna)
    operacoes_de_empilhar = 1

    while not pilha_linhas.pilha_esta_vazia():
        l = pilha_linhas.desempilha()
        c = pilha_colunas.desempilha()
        if not (0 <= l < n_linhas and 0 <= c < n_colunas):
            continue
        if matriz[l][c] != alvo:
            continue
        matriz[l][c] = novo
        for delta_linha, delta_coluna in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            pilha_linhas.empilha(l + delta_linha)
            pilha_colunas.empilha(c + delta_coluna)
            operacoes_de_empilhar += 1

    return operacoes_de_empilhar


def _contar_operacoes_versao_final(matriz, linha, coluna, novo="0", alvo="1"):
    n_linhas, n_colunas = len(matriz), len(matriz[0])

    def dentro(l, c):
        return 0 <= l < n_linhas and 0 <= c < n_colunas

    pilha = Pilha(n_linhas * n_colunas, int)
    matriz[linha][coluna] = novo
    pilha.empilha(linha * n_colunas + coluna)
    operacoes_de_empilhar = 1

    while not pilha.pilha_esta_vazia():
        posicao = pilha.desempilha()
        l, c = divmod(posicao, n_colunas)
        for delta_linha, delta_coluna in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nl, nc = l + delta_linha, c + delta_coluna
            if dentro(nl, nc) and matriz[nl][nc] == alvo:
                matriz[nl][nc] = novo
                pilha.empilha(nl * n_colunas + nc)
                operacoes_de_empilhar += 1

    return operacoes_de_empilhar


def test_pilha_final_faz_muito_menos_operacoes_que_a_versao_ingenua():
    tamanho = 100

    sala_ingenua = _montar_sala(tamanho, tamanho)
    operacoes_ingenuas = _preencher_ingenuo_com_pilhas_paralelas(
        sala_ingenua, tamanho // 2, tamanho // 2
    )

    sala_final = _montar_sala(tamanho, tamanho)
    operacoes_finais = _contar_operacoes_versao_final(sala_final, tamanho // 2, tamanho // 2)

    # a versão final agenda cada célula no máximo uma vez: capacidade exata n*m
    assert operacoes_finais == (tamanho - 2) * (tamanho - 2)
    # a versão ingênua reempilha vizinhos já preenchidos: sempre bem mais operações
    assert operacoes_ingenuas > operacoes_finais * 3

    # e, apesar de fazer mais operações, chega ao mesmo resultado final
    assert sala_ingenua == sala_final


def test_pilha_final_e_mais_rapida_que_a_versao_ingenua():
    tamanho = 200

    tempo_ingenuo = _menor_tempo(
        lambda: _preencher_ingenuo_com_pilhas_paralelas(
            _montar_sala(tamanho, tamanho), tamanho // 2, tamanho // 2
        )
    )
    tempo_final = _menor_tempo(
        lambda: preenchimento_pilha.preencher(
            _montar_sala(tamanho, tamanho), tamanho // 2, tamanho // 2
        )
    )

    assert tempo_final < tempo_ingenuo


# ---------------------------------------------------------------------------
# Versão ingênua do preenchimento recursivo: matriz como lista de strings
# (imutáveis). Cada escrita reconstrói a linha inteira via fatiamento — custo
# O(n_colunas) por célula, em vez de O(1) como na versão final (lista de
# listas de caracteres).
# ---------------------------------------------------------------------------
def _preencher_ingenuo_recursivo_com_strings(matriz, linha, coluna, n_linhas, n_colunas):
    if not (0 <= linha < n_linhas and 0 <= coluna < n_colunas):
        return
    if matriz[linha][coluna] != "1":
        return
    matriz[linha] = matriz[linha][:coluna] + "0" + matriz[linha][coluna + 1:]
    for delta_linha, delta_coluna in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        _preencher_ingenuo_recursivo_com_strings(
            matriz, linha + delta_linha, coluna + delta_coluna, n_linhas, n_colunas
        )


def _preencher_com_listas(matriz, linha, coluna, n_linhas, n_colunas):
    if not (0 <= linha < n_linhas and 0 <= coluna < n_colunas):
        return
    if matriz[linha][coluna] != "1":
        return
    matriz[linha][coluna] = "0"
    for delta_linha, delta_coluna in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        _preencher_com_listas(matriz, linha + delta_linha, coluna + delta_coluna, n_linhas, n_colunas)


def test_recursivo_com_listas_e_mais_rapido_que_com_strings():
    # Muitas salas pequenas (bem abaixo do limite de recursão) para acumular
    # um volume de trabalho grande sem estourar a pilha nativa da thread principal.
    n_salas, tamanho = 300, 25

    def rodar_com_strings():
        for _ in range(n_salas):
            sala = _montar_sala_strings(tamanho, tamanho)
            _preencher_ingenuo_recursivo_com_strings(sala, tamanho // 2, tamanho // 2, tamanho, tamanho)

    def rodar_com_listas():
        for _ in range(n_salas):
            sala = _montar_sala(tamanho, tamanho)
            _preencher_com_listas(sala, tamanho // 2, tamanho // 2, tamanho, tamanho)

    tempo_strings = _menor_tempo(rodar_com_strings)
    tempo_listas = _menor_tempo(rodar_com_listas)

    assert tempo_listas < tempo_strings


def test_recursao_sem_protecao_estoura_em_regiao_grande():
    limite_original = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)
    try:
        tamanho = 60  # sala 60x60: conectada o bastante para passar de 1000 chamadas
        sala = _montar_sala(tamanho, tamanho)
        with pytest.raises(RecursionError):
            _preencher_com_listas(sala, tamanho // 2, tamanho // 2, tamanho, tamanho)
    finally:
        sys.setrecursionlimit(limite_original)


def test_recursivo_final_com_protecao_nao_estoura_na_mesma_regiao():
    tamanho = 60
    sala = _montar_sala(tamanho, tamanho)

    eventos = preenchimento_recursivo.preencher(sala, tamanho // 2, tamanho // 2)

    assert len(eventos) == (tamanho - 2) * (tamanho - 2)


def test_recursivo_final_lida_com_regiao_bem_maior_que_o_limite_padrao():
    tamanho = 250  # 62500 células — bem acima do limite padrão de recursão (1000)
    sala = _montar_sala(tamanho, tamanho)

    eventos = preenchimento_recursivo.preencher(sala, tamanho // 2, tamanho // 2)

    assert len(eventos) == (tamanho - 2) * (tamanho - 2)
