"""Pequenas rotinas de entrada via terminal, sem dependência de tkinter.

Separado de `interface_grafica.py` de propósito: esse módulo importa
`tkinter` no escopo global, e qualquer coisa definida nele fica impossível
de testar em um ambiente sem tkinter instalado. Como pedir a velocidade de
reprodução é só uma validação de número, ela vive aqui — testável mesmo
sem interface gráfica disponível.
"""


def solicitar_velocidade(entrada=input, saida=print):
    """Pede, via terminal, quantas iterações por segundo o modo Play deve usar."""
    while True:
        bruto = entrada("Quantas iterações por segundo no modo Play? ")
        try:
            valor = float(bruto)
        except ValueError:
            saida("Informe um número maior que zero.")
            continue
        if valor > 0:
            return valor
        saida("Informe um número maior que zero.")
