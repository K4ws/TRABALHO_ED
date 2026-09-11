# AGENT.md — Diretrizes Padrão de Entrega

Este arquivo define as regras de entrega que valem para **todo** trabalho/exercício
deste repositório. Sempre que uma nova pasta de trabalho for criada, estas
diretrizes devem ser seguidas e todos os artefatos listados abaixo devem ser
produzidos para aquela pasta.

## Sobre o repositório

Repositório de exercícios desenvolvidos ao longo do período 2026.2 na disciplina
**MAE014 - Tóp. Ciência Dados B [Turmas MAP e EMA]**. Cada trabalho fica em sua
própria pasta na raiz do repositório (ex.: `classe_pilha/`,
`classe_pilha_preenchimento/`, `classe_pilha_torre_hanoi/`), e cada pasta deve
conter, de forma independente, todo o código e todos os relatórios exigidos
para aquela entrega.

> **Estado atual:** os arquivos do trabalho da Pilha (`pilha.py`, `pilha.hpp`,
> `pilha.js`, testes, `POST_MORTEM.md`, `CODE_REVIEW.md`, `ANALISE_CRITICA.md`,
> `RELATORIO_TESTES.md`, `ENTREGA.md`, `ci.yml`) ainda estão soltos na raiz do
> repositório em vez de dentro de `classe_pilha/`. Ao organizar esse trabalho,
> migre-os para lá seguindo a mesma estrutura descrita aqui.

## Integrantes do grupo

| Nome completo | DRE |
|---|---|
| Emanuel Cardoso | 122033151 |
| Alanna Figueiredo Simões | 120053919 |
| Felipe Rodrigues Schoeffer | 123311188 |
| Artur de Melo Brito | 117224234 |
| _(adicionar novo integrante aqui)_ | |

Esta tabela é a fonte de verdade dos nomes/DREs usados na **folha de rosto**
dos relatórios em PDF de todos os trabalhos do repositório. Mantenha-a
atualizada — inclusive em trabalhos já entregues, se o grupo mudar.

## O que cada pasta de trabalho deve conter

```
<pasta_do_trabalho>/
├── python/ , cpp/ , javascript/ ...   # código-fonte por linguagem, quando aplicável
├── ci.yml (ou .github/workflows/ci.yml) # execução automatizada dos testes
├── ENTREGA.md                # checklist de entrega (recomendado)
├── POST_MORTEM.md
├── CODE_REVIEW.md
├── ANALISE_CRITICA.md
├── RELATORIO_TESTES.md
├── POST_MORTEM.pdf            # mesmo conteúdo do .md, com folha de rosto
├── CODE_REVIEW.pdf
├── ANALISE_CRITICA.pdf
└── RELATORIO_TESTES.pdf
```

### 1. Código e testes

- Código-fonte que implementa o que foi pedido no enunciado do trabalho.
- Testes automatizados cobrindo casos normais e casos de erro/borda.
- CI (quando configurado) rodando os testes de cada linguagem usada.

### 2. Relatórios obrigatórios

Os nomes abaixo seguem o padrão já usado neste repositório. Cada um cobre um
dos entregáveis exigidos pela disciplina:

- **`POST_MORTEM.md`** — o documento principal de avaliação de autoria.
  Deve conter, no mínimo, as quatro seções abaixo:
  1. **Log de Iteração e Prompts** — os prompts-chave usados para gerar
     trechos relevantes da solução e os fragmentos de código **brutos**
     devolvidos pela IA, antes de qualquer modificação manual.
  2. **Code Review Crítico** — falhas de eficiência, complexidade de
     algoritmo, vazamentos de memória, falta de índices ou problemas de
     concorrência identificados na solução inicial da IA (pode remeter ao
     `CODE_REVIEW.md` para o detalhamento).
  3. **Justificativa de Refatoração** — o que precisou ser alterado no
     código gerado pela IA para atender aos requisitos de desempenho,
     correção e testes de estresse solicitados.
  4. **Evidência de Testes** — relatório simples dos testes de estresse
     executados, demonstrando que o código refatorado supera o código
     ingênuo gerado inicialmente pela IA (pode remeter ao
     `RELATORIO_TESTES.md`).

- **`CODE_REVIEW.md`** — Relatório de Code Review sobre o código da IA:
  identifica onde a IA gerou código ineficiente (complexidade de algoritmo,
  cópias/percursos desnecessários, falta de validação, uso de estrutura
  inadequada ao enunciado, etc.), comparando a versão ingênua com a versão
  final.

- **`RELATORIO_TESTES.md`** — Relatório de bateria de testes efetuados
  buscando problemas: lista os casos testados (incluindo testes de
  estresse/carga), os comandos usados para executá-los e as
  evidências/saídas obtidas, demonstrando que a versão refatorada supera a
  versão ingênua da IA.

- **`ANALISE_CRITICA.md`** — Análise Crítica do uso da IA: o que a IA ajudou
  a produzir, o que precisou de revisão humana, e os principais riscos de
  aceitar o código da IA sem revisão. Complementa o `POST_MORTEM.md`.

- **`ENTREGA.md`** (opcional, recomendado) — checklist de entrega no padrão
  do arquivo já existente na raiz deste repositório.

> O item "Relatório com o log dos prompts utilizados e o código bruto
> gerado pela IA" já fica coberto pela seção 1 do `POST_MORTEM.md` — não é
> necessário um arquivo separado para isso.

### 3. PDFs com folha de rosto

Os quatro relatórios (`POST_MORTEM`, `CODE_REVIEW`, `ANALISE_CRITICA`,
`RELATORIO_TESTES`) devem ter uma versão em PDF equivalente ao `.md`,
iniciando com uma **FOLHA DE ROSTO** contendo:

- Nome da disciplina (MAE014 - Tóp. Ciência Dados B) e da turma;
- Nome/título do trabalho;
- Nome completo e DRE de cada integrante do grupo (ver tabela acima);
- Data da entrega.

Os arquivos de código não precisam de versão em PDF.

Há uma ferramenta compartilhada para gerar esses PDFs automaticamente a
partir dos `.md`, lendo a tabela de integrantes diretamente deste arquivo:

```bash
pip install reportlab
python scripts/gerar_pdfs.py <pasta_do_trabalho> --titulo "Título do trabalho"
```

Isso gera `POST_MORTEM.pdf`, `CODE_REVIEW.pdf`, `ANALISE_CRITICA.pdf` e
`RELATORIO_TESTES.pdf` dentro da própria pasta do trabalho, cada um já com
a folha de rosto. Mantenha a tabela de integrantes deste arquivo atualizada
antes de gerar os PDFs.

## Processo ao iniciar uma nova pasta de trabalho

1. Criar uma pasta na raiz do repositório com nome descritivo do trabalho.
2. Implementar o código pedido, junto com os testes automatizados.
3. Durante o desenvolvimento com IA, registrar os prompts usados e as
   respostas brutas da IA (antes de qualquer edição manual) — esse material
   alimenta a seção 1 do `POST_MORTEM.md`.
4. Produzir os quatro relatórios `.md` descritos acima, com os nomes
   padronizados.
5. Exportar cada relatório `.md` para `.pdf`, inserindo a folha de rosto com
   os integrantes.
6. Preencher/gerar o `ENTREGA.md` com o checklist específico da pasta.
7. Rodar os testes localmente (e no CI, se configurado) antes do commit/push.

## Observação

Este arquivo consolida as diretrizes de entrega fixadas pela disciplina; elas
se repetem para todos os trabalhos deste repositório. Atualize este arquivo
se o professor alterar algum requisito dos entregáveis.
