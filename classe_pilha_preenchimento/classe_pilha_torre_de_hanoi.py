def interacao(n, movimento, mostrar_jogo):
  if movimento[0] != 7:
    while True:
      try:
        M_input = input('Mover quantos discos: ')
        if not M_input:
          print("Entrada não pode ser vazia. Por favor, digite um número inteiro.")
          continue
        M = int(M_input)
        if M <= 0:
          print("Por favor, digite um número inteiro positivo.")
          continue
        mostrar_jogo[0] = movimento[0] + M
        break
      except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")

    while True:
      usuario = input('Pressione [Enter] para continuar...')
      if usuario == "":
          break
      print("Ops! Você digitou algo. Para continuar, aperte APENAS a tecla Enter.")
  else:
    print('\n Fim do jogo!')



def mostra_pinos(n, pinos, movimento, mostrar_jogo):

  if movimento[0] == mostrar_jogo[0]:
    print(f'\n Quantidade de movimentos = {movimento[0]}')

    for pino in pinos:
      if len(pino._dados) == 0:
        print('[]')
      else:
        print(pino._dados.tolist())


    interacao(n, movimento, mostrar_jogo)




def move(n, pino_origem, pino_destino, pino_intermed, pinos, movimentos, mostrar_jogo):


  if n==1:
    pino_destino.empilha(n)
    pino_origem.desempilha()
    movimentos[0] += 1


    mostra_pinos(n, pinos, movimentos, mostrar_jogo)

  else:
    move(n-1, pino_origem, pino_intermed, pino_destino, pinos, movimentos, mostrar_jogo)

    pino_destino.empilha(n)
    pino_origem.desempilha()
    movimentos[0] += 1


    mostra_pinos(n, pinos, movimentos, mostrar_jogo)

    move(n-1, pino_intermed, pino_destino, pino_origem, pinos, movimentos, mostrar_jogo)

def hanoi(n):

  pino_1 = Pilha(int(n), int)
  pino_2 = Pilha(int(n), int)
  pino_3 = Pilha(int(n), int)

  for i in range(int(n), 0, -1):
    pino_1.empilha(i)


  pinos = [pino_1, pino_2, pino_3]

  movimentos = [0]
  mostrar_jogo = [0]

  print(f'\nMovimentações necessárias: {(2**n - 1)} \n')

  mostra_pinos(n, pinos, movimentos, mostrar_jogo)

  move(n, pino_1, pino_2, pino_3, pinos, movimentos, mostrar_jogo)
