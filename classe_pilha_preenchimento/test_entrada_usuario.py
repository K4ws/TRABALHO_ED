from entrada_usuario import solicitar_velocidade


def test_aceita_numero_positivo_de_primeira():
    entradas = iter(["5"])
    valor = solicitar_velocidade(entrada=lambda _: next(entradas), saida=lambda _: None)
    assert valor == 5.0


def test_rejeita_texto_invalido_e_tenta_de_novo():
    entradas = iter(["abc", "10"])
    mensagens = []
    valor = solicitar_velocidade(entrada=lambda _: next(entradas), saida=mensagens.append)

    assert valor == 10.0
    assert len(mensagens) == 1


def test_rejeita_numero_zero_ou_negativo():
    entradas = iter(["0", "-3", "2.5"])
    mensagens = []
    valor = solicitar_velocidade(entrada=lambda _: next(entradas), saida=mensagens.append)

    assert valor == 2.5
    assert len(mensagens) == 2
