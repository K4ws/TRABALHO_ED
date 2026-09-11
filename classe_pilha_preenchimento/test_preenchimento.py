import os

import pytest

import preenchimento_pilha
import preenchimento_recursivo
from matriz_io import copiar_matriz, ler_matriz

PASTA_MATRIZES = os.path.join(os.path.dirname(__file__), "matrizes")

ALGORITMOS = {
    "recursivo": preenchimento_recursivo.preencher,
    "pilha": preenchimento_pilha.preencher,
}


def _caminho(nome_arquivo):
    return os.path.join(PASTA_MATRIZES, nome_arquivo)


@pytest.fixture(params=sorted(ALGORITMOS))
def algoritmo(request):
    return ALGORITMOS[request.param]


def test_figura_pequena_preenche_regiao_conectada(algoritmo):
    matriz, posicao_inicial = ler_matriz(_caminho("figura_pequena.txt"))
    eventos = algoritmo(matriz, *posicao_inicial)

    # Contagem obtida por um preenchimento de referência (verificado manualmente
    # a partir do exemplo do enunciado): 33 células conectadas a X por 4-vizinhança.
    assert len(eventos) == 33
    assert len(set(eventos)) == 33  # nenhuma posição preenchida mais de uma vez

    linha_inicial, coluna_inicial = posicao_inicial
    assert matriz[linha_inicial][coluna_inicial] == "0"


def test_figura_pequena_nao_extrapola_ilha_isolada(algoritmo):
    # A célula (2, 3) do exemplo do enunciado é um "1" cercado por "0" nos
    # quatro lados (uma ilha de um elemento). Ela não é alcançável a partir
    # de X por 4-vizinhança e deve permanecer sem preencher.
    matriz, posicao_inicial = ler_matriz(_caminho("figura_pequena.txt"))
    algoritmo(matriz, *posicao_inicial)

    assert matriz[2][3] == "1"


def test_figura_pequena_borda_permanece_intacta(algoritmo):
    matriz, posicao_inicial = ler_matriz(_caminho("figura_pequena.txt"))
    algoritmo(matriz, *posicao_inicial)

    assert all(c == "1" for c in matriz[0])
    assert all(c == "1" for c in matriz[-1])


def test_figura_aberta_vaza_para_toda_a_regiao_alcancavel(algoritmo):
    matriz, posicao_inicial = ler_matriz(_caminho("figura_pequena_aberta.txt"))
    eventos = algoritmo(matriz, *posicao_inicial)

    # Com a borda aberta em (2, 4), o preenchimento deve escapar da figura e
    # tomar toda a região de "1"s alcançável (verificado manualmente: 158
    # das 192 células — as 34 restantes já eram "0", parte do desenho original).
    assert len(eventos) == 158


def test_labirinto_preenche_regiao_conectada_a_x(algoritmo):
    matriz, posicao_inicial = ler_matriz(_caminho("labirinto.txt"))
    eventos = algoritmo(matriz, *posicao_inicial)

    assert len(eventos) == 502
    linha_inicial, coluna_inicial = posicao_inicial
    assert matriz[linha_inicial][coluna_inicial] == "0"


def test_posicao_inicial_fora_dos_limites_nao_faz_nada(algoritmo):
    matriz, _ = ler_matriz(_caminho("figura_pequena.txt"))
    original = copiar_matriz(matriz)

    eventos = algoritmo(matriz, -1, 0)

    assert eventos == []
    assert matriz == original


def test_posicao_inicial_no_fundo_externo_tambem_preenche(algoritmo):
    # (0, 0) é '1' de fundo, fora da figura — não é o X do enunciado, mas é
    # uma célula "alvo" válida, então o algoritmo deve preenchê-la normalmente.
    matriz, _ = ler_matriz(_caminho("figura_pequena.txt"))
    original = copiar_matriz(matriz)

    eventos = algoritmo(matriz, 0, 0)

    assert len(eventos) > 0
    assert matriz != original


def test_posicao_inicial_sobre_parede_nao_faz_nada(algoritmo):
    matriz, _ = ler_matriz(_caminho("figura_pequena.txt"))
    original = copiar_matriz(matriz)

    assert matriz[1][2] == "0"  # célula de parede real da figura do enunciado
    eventos = algoritmo(matriz, 1, 2)

    assert eventos == []
    assert matriz == original


def test_posicao_inicial_sobre_celula_ja_preenchida_nao_faz_nada(algoritmo):
    matriz, posicao_inicial = ler_matriz(_caminho("figura_pequena.txt"))
    matriz[0][0] = "0"
    original = copiar_matriz(matriz)

    eventos = algoritmo(matriz, 0, 0)

    assert eventos == []
    assert matriz == original


def test_recursivo_e_pilha_concordam_no_resultado_final():
    for nome_arquivo in ("figura_pequena.txt", "figura_pequena_aberta.txt", "labirinto.txt"):
        matriz_recursiva, posicao_inicial = ler_matriz(_caminho(nome_arquivo))
        matriz_pilha = copiar_matriz(matriz_recursiva)

        preenchimento_recursivo.preencher(matriz_recursiva, *posicao_inicial)
        preenchimento_pilha.preencher(matriz_pilha, *posicao_inicial)

        assert matriz_recursiva == matriz_pilha, f"divergência em {nome_arquivo}"
