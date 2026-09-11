"""Reprodução textual do preenchimento — independente do algoritmo utilizado.

Este módulo não sabe (nem precisa saber) se os eventos vieram do algoritmo
recursivo ou do algoritmo com pilha: ele só consome a lista ordenada de
posições preenchidas e uma cópia da matriz original. Essa separação é o que
permite reutilizar o mesmo mecanismo de exibição passo a passo para
qualquer algoritmo que produza esse mesmo contrato (lista de eventos).
"""

from matriz_io import copiar_matriz, exibir_matriz


def reproduzir_no_terminal(matriz_original, eventos, passos_por_pausa, novo="0", entrada=input):
    """Reproduz `eventos` sobre uma cópia de `matriz_original`, no terminal.

    A cada `passos_por_pausa` eventos aplicados, a matriz é exibida e o
    programa aguarda um ENTER do usuário antes de aplicar o próximo bloco.
    Se `passos_por_pausa` for 0, todos os eventos são aplicados de uma vez
    e apenas o resultado final é exibido (sem paradas intermediárias).

    Devolve a matriz final (já com o preenchimento aplicado).
    """
    matriz = copiar_matriz(matriz_original)
    total = len(eventos)

    if passos_por_pausa < 0:
        raise ValueError("passos_por_pausa não pode ser negativo.")

    if passos_por_pausa == 0:
        for l, c in eventos:
            matriz[l][c] = novo
        exibir_matriz(matriz, titulo="Matriz depois do preenchimento:")
        return matriz

    indice = 0
    while True:
        fim = min(indice + passos_por_pausa, total)
        for l, c in eventos[indice:fim]:
            matriz[l][c] = novo
        indice = fim

        titulo = (
            "Matriz depois do preenchimento:"
            if indice == total
            else f"Matriz após {indice}/{total} passos:"
        )
        exibir_matriz(matriz, titulo=titulo)

        if indice >= total:
            return matriz
        entrada(f"[{indice}/{total} passos] Pressione ENTER para continuar... ")
