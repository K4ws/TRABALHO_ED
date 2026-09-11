import pytest

from matriz_io import copiar_matriz
from reprodutor import reproduzir_no_terminal


def _matriz_5x5_toda_aberta():
    return [list("11111") for _ in range(5)]


def test_passos_zero_aplica_tudo_de_uma_vez_sem_pausas(capsys):
    matriz = _matriz_5x5_toda_aberta()
    eventos = [(l, c) for l in range(5) for c in range(5)]
    chamadas_entrada = []

    resultado = reproduzir_no_terminal(
        matriz, eventos, passos_por_pausa=0, entrada=lambda *_: chamadas_entrada.append(1)
    )

    assert chamadas_entrada == []  # nenhuma pausa, mesmo com muitos eventos
    assert all(c == "0" for linha in resultado for c in linha)

    saida = capsys.readouterr().out
    assert "Matriz depois do preenchimento:" in saida
    assert "passos:" not in saida  # não deve haver apresentações intermediárias


def test_passos_positivos_pausa_entre_blocos_e_aguarda_entrada(capsys):
    matriz = _matriz_5x5_toda_aberta()
    eventos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    chamadas_entrada = []

    resultado = reproduzir_no_terminal(
        matriz, eventos, passos_por_pausa=2, entrada=lambda *_: chamadas_entrada.append(1)
    )

    # 5 eventos em blocos de 2: [0:2], [2:4], [4:5] -> 3 apresentações, 2 pausas
    assert len(chamadas_entrada) == 2

    saida = capsys.readouterr().out
    assert "Matriz após 2/5 passos:" in saida
    assert "Matriz após 4/5 passos:" in saida
    assert "Matriz depois do preenchimento:" in saida

    assert resultado[0][:5] == ["0", "0", "0", "0", "0"]


def test_matriz_original_nao_e_alterada():
    matriz_original = _matriz_5x5_toda_aberta()
    copia_para_comparar = copiar_matriz(matriz_original)
    eventos = [(0, 0), (1, 1)]

    reproduzir_no_terminal(matriz_original, eventos, passos_por_pausa=0, entrada=lambda *_: None)

    assert matriz_original == copia_para_comparar


def test_passos_negativos_geram_erro():
    matriz = _matriz_5x5_toda_aberta()
    with pytest.raises(ValueError):
        reproduzir_no_terminal(matriz, [], passos_por_pausa=-1, entrada=lambda *_: None)
