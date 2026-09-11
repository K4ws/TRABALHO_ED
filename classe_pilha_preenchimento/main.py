"""Ponto de entrada: lê a matriz, escolhe o algoritmo e reproduz o preenchimento.

Uso:
    python main.py matrizes/figura_pequena.txt --algoritmo pilha --passos 5
    python main.py matrizes/labirinto.txt --algoritmo recursivo --interface grafica
"""

import argparse
import sys

import preenchimento_pilha
import preenchimento_recursivo
from matriz_io import copiar_matriz, exibir_matriz, ler_matriz
from reprodutor import reproduzir_no_terminal

ALGORITMOS = {
    "recursivo": preenchimento_recursivo.preencher,
    "pilha": preenchimento_pilha.preencher,
}


def analisar_argumentos(argv=None):
    analisador = argparse.ArgumentParser(
        description="Preenchimento de região em matriz de caracteres (0's e 1's)."
    )
    analisador.add_argument("arquivo", help="Caminho do arquivo de texto com a matriz.")
    analisador.add_argument(
        "--algoritmo", choices=sorted(ALGORITMOS), default="pilha",
        help="Algoritmo de preenchimento a utilizar (padrão: pilha).",
    )
    analisador.add_argument(
        "--passos", type=int, default=0,
        help="Quantidade de passos entre cada apresentação da matriz no modo texto "
             "(0 = executar até o fim, sem paradas intermediárias).",
    )
    analisador.add_argument(
        "--interface", choices=["texto", "grafica"], default="texto",
        help="Modo de reprodução: texto no terminal ou janela gráfica (bitmap).",
    )
    return analisador.parse_args(argv)


def main(argv=None):
    argumentos = analisar_argumentos(argv)

    matriz_original, posicao_inicial = ler_matriz(argumentos.arquivo)
    if posicao_inicial is None:
        print("O arquivo não contém uma posição inicial marcada com 'X'.", file=sys.stderr)
        return 1

    exibir_matriz(matriz_original, titulo="Matriz antes do preenchimento:")

    matriz_de_trabalho = copiar_matriz(matriz_original)
    preencher = ALGORITMOS[argumentos.algoritmo]
    eventos = preencher(matriz_de_trabalho, *posicao_inicial)

    if argumentos.interface == "texto":
        reproduzir_no_terminal(matriz_original, eventos, argumentos.passos)
        return 0

    from entrada_usuario import solicitar_velocidade
    import interface_grafica  # importado só aqui: modo texto não exige tkinter instalado

    velocidade = solicitar_velocidade()
    janela = interface_grafica.JanelaPreenchimento(matriz_original, eventos, velocidade)
    janela.executar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
