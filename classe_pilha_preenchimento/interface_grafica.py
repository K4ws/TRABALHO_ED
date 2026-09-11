"""Janela gráfica (bitmap de pixels) para reproduzir o preenchimento.

Assim como `reprodutor.py`, esta janela só depende de uma matriz original e
de uma lista ordenada de eventos (linha, coluna) — o mesmo contrato
produzido tanto por `preenchimento_recursivo.preencher` quanto por
`preenchimento_pilha.preencher`. O algoritmo, a interface de texto e esta
interface gráfica são módulos independentes: qualquer um pode ser trocado
sem alterar os outros dois.

Requer o módulo padrão `tkinter` (normalmente disponível em instalações
"completas" do Python; algumas instalações mínimas de Linux não o incluem
por padrão — nesse caso, instale o pacote do sistema, ex.: `python3-tk`).
"""

import tkinter as tk

from matriz_io import copiar_matriz

PALETA_PADRAO = {"1": "#f5f5f5", "0": "#e63946"}
COR_PADRAO = "#ffffff"
COR_GRADE = "#cccccc"
TAMANHO_CELULA_PADRAO = 16


class JanelaPreenchimento:
    """Reproduz eventos de preenchimento em um bitmap de pixels (grade de retângulos)."""

    def __init__(
        self,
        matriz_original,
        eventos,
        iteracoes_por_segundo,
        novo="0",
        paleta=None,
        tamanho_celula=TAMANHO_CELULA_PADRAO,
    ):
        if iteracoes_por_segundo <= 0:
            raise ValueError("iteracoes_por_segundo deve ser maior que zero.")

        self._matriz = copiar_matriz(matriz_original)
        self._eventos = eventos
        self._indice = 0
        self._novo = novo
        self._paleta = {**PALETA_PADRAO, **(paleta or {})}
        self._em_reproducao = False
        self._intervalo_ms = max(1, round(1000 / iteracoes_por_segundo))

        n_linhas = len(self._matriz)
        n_colunas = len(self._matriz[0]) if n_linhas else 0
        self._tamanho_celula = tamanho_celula

        self._janela = tk.Tk()
        self._janela.title("Preenchimento de região — reprodução")

        self._canvas = tk.Canvas(
            self._janela,
            width=n_colunas * tamanho_celula,
            height=n_linhas * tamanho_celula,
            highlightthickness=0,
        )
        self._canvas.pack()
        self._retangulos = self._desenhar_bitmap_inicial()

        barra = tk.Frame(self._janela)
        barra.pack(fill="x")
        self._botao_play = tk.Button(barra, text="Play", command=self._alternar_reproducao)
        self._botao_play.pack(side="left", padx=4, pady=4)
        self._botao_passo = tk.Button(barra, text="Passo", command=self._avancar_um_passo)
        self._botao_passo.pack(side="left", padx=4, pady=4)
        self._rotulo_status = tk.Label(barra, text=self._texto_status())
        self._rotulo_status.pack(side="left", padx=8)

    def _desenhar_bitmap_inicial(self):
        retangulos = []
        t = self._tamanho_celula
        for l, linha in enumerate(self._matriz):
            linha_retangulos = []
            for c, caractere in enumerate(linha):
                cor = self._paleta.get(caractere, COR_PADRAO)
                retangulo = self._canvas.create_rectangle(
                    c * t, l * t, (c + 1) * t, (l + 1) * t, fill=cor, outline=COR_GRADE
                )
                linha_retangulos.append(retangulo)
            retangulos.append(linha_retangulos)
        return retangulos

    def _texto_status(self):
        return f"{self._indice}/{len(self._eventos)} passos"

    def _aplicar_evento(self, linha, coluna):
        self._matriz[linha][coluna] = self._novo
        cor = self._paleta.get(self._novo, COR_PADRAO)
        self._canvas.itemconfig(self._retangulos[linha][coluna], fill=cor)

    def _avancar_um_passo(self):
        if self._indice >= len(self._eventos):
            return
        linha, coluna = self._eventos[self._indice]
        self._aplicar_evento(linha, coluna)
        self._indice += 1
        self._rotulo_status.config(text=self._texto_status())

    def _alternar_reproducao(self):
        self._em_reproducao = not self._em_reproducao
        self._botao_play.config(text="Pausar" if self._em_reproducao else "Play")
        self._botao_passo.config(state="disabled" if self._em_reproducao else "normal")
        if self._em_reproducao:
            self._tick()

    def _tick(self):
        if not self._em_reproducao:
            return
        if self._indice >= len(self._eventos):
            self._pausar()
            return
        self._avancar_um_passo()
        self._janela.after(self._intervalo_ms, self._tick)

    def _pausar(self):
        self._em_reproducao = False
        self._botao_play.config(text="Play")
        self._botao_passo.config(state="normal")

    def executar(self):
        self._janela.mainloop()
