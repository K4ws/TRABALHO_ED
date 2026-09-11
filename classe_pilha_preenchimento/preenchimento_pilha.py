"""Preenchimento de região usando uma pilha explícita de posições (linha, coluna).

Reaproveita a classe `Pilha` de `pilha.py`. Como essa pilha só aceita um
tipo básico por instância (int, float ou str — ver PilhaCheiaErro/TipoErro
em pilha.py), cada posição (linha, coluna) é codificada em um único inteiro
`linha * n_colunas + coluna` e desempilhada com `divmod`. Isso permite usar
uma única `Pilha(capacidade, int)` para armazenar posições compostas, em
vez de duas pilhas paralelas (uma de linhas, outra de colunas) — a
alternativa mais direta, mas menos eficiente e mais frágil, descrita em
CODE_REVIEW.md.

Uma célula só é empilhada quando ainda é `alvo` (isto é, no momento em que
é descoberta como vizinha de uma célula já processada), e é marcada como
preenchida imediatamente. Isso garante que cada célula é empilhada no
máximo uma vez, o que permite dimensionar a pilha com a capacidade exata
`n_linhas * n_colunas`, sem estimativas por excesso.
"""

from matriz_io import VIZINHANCA_4
from pilha import Pilha


def preencher(matriz, linha, coluna, novo="0", alvo="1"):
    """Preenche, com uma pilha explícita, a região de `alvo`s conectada a (linha, coluna).

    Altera `matriz` em memória e devolve a lista ordenada das posições
    preenchidas (na ordem em que foram desempilhadas), usada pelos
    reprodutores (texto ou interface gráfica) para repetir a evolução do
    algoritmo passo a passo.
    """
    n_linhas = len(matriz)
    n_colunas = len(matriz[0]) if n_linhas else 0

    def dentro_dos_limites(l, c):
        return 0 <= l < n_linhas and 0 <= c < n_colunas

    if not dentro_dos_limites(linha, coluna) or matriz[linha][coluna] != alvo:
        return []

    def codificar(l, c):
        return l * n_colunas + c

    pilha = Pilha(n_linhas * n_colunas, int)
    eventos = []

    matriz[linha][coluna] = novo
    eventos.append((linha, coluna))
    pilha.empilha(codificar(linha, coluna))

    while not pilha.pilha_esta_vazia():
        posicao = pilha.desempilha()
        l, c = divmod(posicao, n_colunas)
        for delta_linha, delta_coluna in VIZINHANCA_4:
            nl, nc = l + delta_linha, c + delta_coluna
            if dentro_dos_limites(nl, nc) and matriz[nl][nc] == alvo:
                matriz[nl][nc] = novo
                eventos.append((nl, nc))
                pilha.empilha(codificar(nl, nc))

    return eventos
