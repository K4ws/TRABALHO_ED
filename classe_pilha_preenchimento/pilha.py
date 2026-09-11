from array import array


class PilhaCheiaErro(Exception):
    """Indica que a pilha atingiu sua capacidade máxima."""


class PilhaVaziaErro(Exception):
    """Indica que foi solicitada uma operação em uma pilha vazia."""


class TipoErro(Exception):
    """Indica que o dado não pertence ao tipo configurado para a pilha."""


class Pilha:
    """
    Implementa uma pilha de capacidade fixa usando array da biblioteca padrão.

    tipo pode ser int, float ou str. Quando tipo=str, somente caracteres
    de comprimento 1 são aceitos.
    """

    _TIPOS = {
        int: "i",
        float: "d",
        str: "u",
    }

    def __init__(self, capacidade, tipo):
        if not isinstance(capacidade, int) or isinstance(capacidade, bool) or capacidade <= 0:
            raise ValueError("A capacidade deve ser um inteiro positivo.")
        if tipo not in self._TIPOS:
            raise ValueError("O tipo deve ser int, float ou str.")

        self._capacidade = capacidade
        self._tipo = tipo
        self._dados = array(self._TIPOS[tipo])

    def empilha(self, dado):
        """Empilha dado no topo."""
        if self.pilha_esta_cheia():
            raise PilhaCheiaErro("A pilha está cheia.")
        if not self._tipo_valido(dado):
            raise TipoErro(f"Dado incompatível com o tipo {self._tipo.__name__}.")
        self._dados.append(dado)

    def desempilha(self):
        """Remove e retorna o elemento do topo."""
        if self.pilha_esta_vazia():
            raise PilhaVaziaErro("A pilha está vazia.")
        return self._dados.pop()

    def Desempilha(self):
        """Nome alternativo conforme a especificação do trabalho."""
        return self.desempilha()

    def pilha_esta_vazia(self):
        return len(self._dados) == 0

    def pilha_esta_cheia(self):
        return len(self._dados) == self._capacidade

    def troca(self):
        """Troca o topo com o elemento imediatamente abaixo dele."""
        if len(self._dados) < 2:
            raise PilhaVaziaErro("São necessários pelo menos dois elementos para trocar.")
        self._dados[-1], self._dados[-2] = self._dados[-2], self._dados[-1]

    def tamanho(self):
        return len(self._dados)

    def _tipo_valido(self, dado):
        if self._tipo is int:
            return isinstance(dado, int) and not isinstance(dado, bool)
        if self._tipo is float:
            return isinstance(dado, (int, float)) and not isinstance(dado, bool)
        return isinstance(dado, str) and len(dado) == 1
