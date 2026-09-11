"""Leitura, cópia e exibição textual de matrizes de caracteres."""

VIZINHANCA_4 = ((-1, 0), (1, 0), (0, -1), (0, 1))

MAPA_TEXTO_PADRAO = {"1": " ", "0": "@"}


def ler_matriz(caminho, marcador_inicial="X"):
    """Lê um arquivo texto e devolve (matriz, posicao_inicial).

    Cada linha do arquivo vira uma lista de caracteres (mutável), permitindo
    que os algoritmos de preenchimento alterem células individualmente. Se
    houver um caractere igual a `marcador_inicial`, ele indica a posição
    inicial do preenchimento — a célula correspondente é normalizada para
    '1' na matriz devolvida (a posição inicial deve ser uma célula aberta).
    Se o marcador não existir no arquivo, `posicao_inicial` é None.
    """
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = [linha.rstrip("\r\n") for linha in arquivo]
    linhas = [linha for linha in linhas if linha != ""]

    matriz = [list(linha) for linha in linhas]
    posicao_inicial = None
    for l, linha in enumerate(matriz):
        for c, caractere in enumerate(linha):
            if caractere == marcador_inicial:
                posicao_inicial = (l, c)
                matriz[l][c] = "1"

    return matriz, posicao_inicial


def copiar_matriz(matriz):
    return [linha.copy() for linha in matriz]


def formatar_linha(linha, mapa=MAPA_TEXTO_PADRAO):
    return "".join(mapa.get(caractere, caractere) for caractere in linha)


def exibir_matriz(matriz, titulo=None, mapa=MAPA_TEXTO_PADRAO, arquivo=None):
    if titulo:
        print(titulo, file=arquivo)
    for linha in matriz:
        print(formatar_linha(linha, mapa), file=arquivo)
    print(file=arquivo)
