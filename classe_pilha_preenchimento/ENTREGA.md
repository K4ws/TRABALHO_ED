# Checklist de Entrega

## Identificação
- [x] Nome(s) do(s) integrante(s) e DRE(s) — ver `AGENT.md` na raiz do repositório
- [ ] Link do GitHub Classroom / GitLab CI

## Código
- [x] Classe `Pilha` reaproveitada — `pilha.py`
- [x] Algoritmo recursivo — `preenchimento_recursivo.py`
- [x] Algoritmo com pilha de posições — `preenchimento_pilha.py`
- [x] Leitura/exibição de matriz — `matriz_io.py`
- [x] Reprodução em texto (P passos, ENTER) — `reprodutor.py`
- [x] Interface gráfica (bitmap, Play/Passo, cores) — `interface_grafica.py`
- [x] Entrada de velocidade via terminal (testável sem tkinter) — `entrada_usuario.py`
- [x] Orquestração / CLI — `main.py`
- [x] Matrizes de exemplo — `matrizes/figura_pequena.txt`, `matrizes/figura_pequena_aberta.txt`, `matrizes/labirinto.txt`
- [x] CI — `ci.yml` (mover para `.github/workflows/ci.yml` na raiz do repositório para ativar no GitHub Actions)

## Testes
- [x] Testes funcionais — `test_preenchimento.py`, `test_reprodutor.py`, `test_entrada_usuario.py`
- [x] Testes de estresse (ingênuo vs. final) — `test_estresse.py`

## Documentação
- [x] `POST_MORTEM.md`
- [x] `CODE_REVIEW.md`
- [x] `ANALISE_CRITICA.md`
- [x] `RELATORIO_TESTES.md`
- [ ] PDFs dos quatro relatórios acima, com folha de rosto (gerar com `scripts/gerar_pdfs.py` na raiz do repositório)

## Antes de enviar
1. Rodar `python -m pytest -v` dentro de `classe_pilha_preenchimento/` no ambiente do grupo.
2. Testar a interface gráfica (`python main.py <matriz> --interface grafica`) em uma máquina com `tkinter` e ambiente gráfico — não validado no ambiente de preparação (container sem `tkinter`/display).
3. Preencher nomes, DREs e link do repositório.
4. Gerar os PDFs dos relatórios com a folha de rosto e conferir o conteúdo.
5. Conferir o histórico do Git e fazer o push do repositório.
