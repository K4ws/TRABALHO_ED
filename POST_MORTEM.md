# POST MORTEM: Implementação da Estrutura de Dados Pilha (POO)

## Integrantes do Grupo

| **Nome completo** | **DRE** |
|---|---:|
| Emanuel Cardoso | 122033151 |
| Alanna Figueiredo Simões | 120053919 |
| Felipe Rodrigues Schoeffer | 123311188 |
| Artur de Melo Brito | 117224234 |
| Matheus de Sousa | 123536584 |

---

## 1. Visão Geral do Projeto

Este documento apresenta o relatório técnico pós-desenvolvimento (*Post
Mortem*) e a análise crítica da refatoração da estrutura de dados
**Pilha** com capacidade estática em memória contígua e tipagem rígida.

O projeto foi desenvolvido em três linguagens de programação:

-   **Python**
-   **C**
-   **JavaScript**

O trabalho consiste no desenvolvimento de uma estrutura de dados do tipo
**Pilha (Stack)** utilizando Programação Orientada a Objetos ou uma estrutura
equivalente, seguindo os princípios de **LIFO (Last In, First Out)**. A pilha
deve possuir capacidade estática, utilizar armazenamento contíguo e aceitar
somente dados de um único tipo básico por instância: **caractere, inteiro ou
ponto flutuante**.

O projeto foi implementado em **Python, C e JavaScript**, permitindo comparar
como cada linguagem trata memória, tipagem, estruturas de armazenamento e
controle de recursos. Para cada linguagem foram produzidas uma versão inicial,
gerada com auxílio de Inteligência Artificial, e uma versão final refatorada
após a realização de um *Code Review*.

Durante a refatoração, foram corrigidos problemas como uso de estruturas
dinâmicas, ausência de validação de tipos, tratamento incompleto de exceções
e gerenciamento inadequado de memória. A versão final busca atender aos
requisitos do trabalho, mantendo as operações da pilha em **O(1)** e
utilizando mecanismos apropriados de armazenamento em cada linguagem.

O objetivo principal foi vivenciar a transição entre uma implementação
inicial ingênua, gerada com auxílio de Inteligência Artificial e focada
apenas na funcionalidade, e uma versão final refatorada de acordo com os
requisitos de engenharia de software.

Entre os principais requisitos considerados estão:

-   complexidade temporal estritamente **O(1)**;
-   armazenamento em memória contígua;
-   capacidade estática e pré-alocada;
-   tipagem rígida;
-   tratamento estruturado de exceções customizadas;
-   gerenciamento adequado dos recursos.

------------------------------------------------------------------------

## 2. Estrutura do Repositório

``` text
projeto_pilha/
│
├── c/
│   ├── pilha_inicial.c
│   └── pilha_refatorada.c
│
├── python/
│   ├── pilha_inicial.py
│   └── pilha_refatorada.py
│
├── javascript/
│   ├── pilha_inicial.js
│   └── pilha_refatorada.js
│
└── POST_MORTEM.md
```

### Descrição dos arquivos

  -----------------------------------------------------------------------
  Pasta/Arquivo                       Descrição
  ----------------------------------- -----------------------------------
  `c/pilha_inicial.c`                 Implementação inicial em C,
                                      utilizando `realloc()` e aceitando
                                      apenas `int`.

  `c/pilha_refatorada.c`              Implementação refatorada em C,
                                      utilizando alocação prévia,
                                      `union`/`enum` e testes.

  `python/pilha_inicial.py`           Implementação inicial em Python
                                      utilizando lista nativa.

  `python/pilha_refatorada.py`        Implementação refatorada em Python
                                      utilizando o módulo `array` e
                                      testes.

  `javascript/pilha_inicial.js`       Implementação inicial em JavaScript
                                      utilizando `Array` dinâmico.

  `javascript/pilha_refatorada.js`    Implementação refatorada utilizando
                                      `TypedArray` e testes.

  `POST_MORTEM.md`                    Relatório técnico consolidado do
                                      projeto.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 3. Log de Iteração e Prompts

## 3.1 Prompt Enviado ao Modelo de IA

> Desenvolva uma classe em Orientação a Objetos (ou TAD equivalente) que
> implemente uma estrutura de dados Pilha de capacidade estática. A
> pilha deve aceitar apenas dados de um mesmo tipo básico (caractere,
> inteiro ou ponto flutuante). O armazenamento interno deve utilizar um
> array contíguo em memória prealocado no construtor. A interface da
> classe deve conter obrigatoriamente os métodos: `empilha(dado)`,
> `desempilha()`, `pilha_esta_vazia()`, `pilha_esta_cheia()`, `troca()`
> e `tamanho()`. Trate as condições de erro disparando as exceções
> customizadas `PilhaCheiaErro`, `PilhaVaziaErro` e `TipoErro`.

## 3.2 Resumo do Código Bruto Gerado pela IA

### Python

A IA instanciou `self.dados = []`, utilizando uma lista nativa
heterogênea.

-   O empilhamento utilizava `.append()`.
-   A remoção utilizava `.pop()`.
-   Não havia validação rígida de tipo.
-   Não havia limitação de tamanho para caracteres.

### C

A IA criou uma `struct` com `int* dados = NULL`.

-   O construtor não alocava a capacidade total.
-   A função `empilha()` utilizava `realloc()` a cada chamada.
-   Apenas o tipo `int` era aceito.

### JavaScript

A IA criou uma classe com `this.dados = []`, utilizando o `Array`
dinâmico padrão do V8.

-   A inserção utilizava `.push()`.
-   A remoção utilizava `.pop()`.
-   O método `troca()` encerrava silenciosamente quando a pilha possuía
    menos de dois elementos.
-   Não era disparada uma exceção nessa situação.

------------------------------------------------------------------------

# 4. Code Review Crítico das Soluções Iniciais da IA

## 4.1 Uso Indevido de Alocação Dinâmica e Quebra da Complexidade O(1)

Em Python e JavaScript, o uso de listas/arrays nativos sujeita o código
a realocações dinâmicas de memória em tempo de execução.

Em C, o uso de `realloc()` a cada chamada de `empilha()` destruiu o
requisito de reserva física prévia.

Isso comprometeu a garantia de tempo constante **O(1) determinístico**.

## 4.2 Falta de Tipagem Rígida e Falha no Suporte a Caracteres

As coleções padrão do Python e JavaScript aceitam múltiplos tipos
misturados dentro da mesma instância.

O código inicial:

-   não validava se a pilha continha apenas um tipo básico;
-   permitia o empilhamento de strings longas em instâncias destinadas a
    `char`;
-   em C, ficou limitado exclusivamente ao tipo `int`.

## 4.3 Gerenciamento de Memória Frágil e Risco de Leaks em C

Ao inicializar o ponteiro como `NULL` e depender do `realloc()`, falhas
de alocação durante a execução poderiam causar problemas de
gerenciamento do ponteiro e risco de vazamento de memória (*memory
leak*).

## 4.4 Tratamento Omisso e Incompleto de Exceções

O método `troca()` nas três linguagens limitava-se a condicionais
simples.

Quando executado em pilhas com menos de dois elementos, o código inicial
finalizava sem alterar o estado e sem disparar a exceção
`PilhaVaziaErro`, mascarando possíveis falhas de execução.

------------------------------------------------------------------------

# 5. Justificativa Técnico-Teórica da Refatoração

## 5.1 Refatoração em Python

### Armazenamento e Tipagem

A lista `[]` foi substituída pelo módulo nativo `array`:

-   `array('q')` para inteiros;
-   `array('d')` para ponto flutuante;
-   `array('u')` para caracteres.

O vetor é pré-alocado no tamanho máximo exato no momento da instanciação
(`__init__`).

### Controle de Índices

Foram eliminados `.append()` e `.pop()`.

O topo da pilha é gerenciado estritamente pela variável
`self.quantidade`.

### Validação de `char`

Foi adicionada uma validação exigindo que valores do tipo `str` tenham
exatamente um caractere:

``` python
len(dado) == 1
```

------------------------------------------------------------------------

## 5.2 Refatoração em Linguagem C

### Alocação Estática Única

A função `criar_pilha()` reserva o bloco contíguo total no heap
utilizando:

``` c
malloc(capacidade * sizeof(Elemento))
```

A alocação ocorre no construtor, evitando realocações durante as
operações da pilha.

### Polimorfismo com Restrição de Tipo

Foi criada uma combinação de:

-   `union Elemento`;
-   `enum TipoDado`.

A pilha pode armazenar diferentes tipos básicos, mas os acessos são
validados de acordo com o tipo configurado no construtor.

### Destruição Segura

A função `destruir_pilha()` garante a desalocação completa do vetor de
dados e do ponteiro principal, prevenindo *memory leaks*.

------------------------------------------------------------------------

## 5.3 Refatoração em JavaScript

### Uso de TypedArray

O `Array` nativo foi substituído por instâncias de:

-   `Int32Array`;
-   `Float64Array`;
-   `Uint16Array`.

Essas estruturas utilizam um `ArrayBuffer` de tamanho fixo para o
armazenamento dos dados.

### Tratamento de Caractere em Buffer Binário

Strings de tamanho 1 são convertidas para seus *code units* UTF-16
utilizando:

``` javascript
charCodeAt(0)
```

No desempilhamento, os valores são reconstruídos utilizando:

``` javascript
String.fromCharCode()
```

### Controle Manual

As operações de inserção e remoção são realizadas por manipulação do
índice:

``` javascript
this.quantidade
```

Dessa forma, são eliminados `.push()` e `.pop()`.

------------------------------------------------------------------------

# 6. Evidência e Relatório dos Testes de Estresse

A bateria de testes automatizados submeteu as implementações refatoradas
a quatro cenários críticos.

## 6.1 Teste de Transbordo de Capacidade --- Overflow

**Ação:** tentativa de empilhar elementos além da capacidade estática
máxima configurada.

**Resultado:** em todas as linguagens, o controle de quantidade bloqueou
a alteração além da capacidade e disparou a exceção `PilhaCheiaErro`.

------------------------------------------------------------------------

## 6.2 Teste de Subflutuação de Memória --- Underflow

**Ação:** invocação de `desempilha()` em pilhas vazias e chamada de
`troca()` em pilhas com 0 ou 1 elemento.

**Resultado:** ocorreu a interceptação imediata com disparo da exceção
customizada `PilhaVaziaErro`, impedindo acessos inválidos à estrutura.

------------------------------------------------------------------------

## 6.3 Teste de Injeção de Tipos Incompatíveis

**Ação:** tentativa de empilhar valores flutuantes ou strings em pilhas
declaradas para inteiros, além da inserção de strings longas em pilhas
de caracteres.

**Resultado:** os valores incompatíveis foram interceptados e bloqueados
pela verificação estrita de tipagem, disparando a exceção `TipoErro`.

------------------------------------------------------------------------

## 6.4 Teste da Operação `troca()` e Consistência LIFO

**Ação:** inserção de elementos, execução do método `troca()` e
desempilhamento sequencial.

**Resultado:** a inversão do elemento do topo com o imediatamente abaixo
ocorreu com sucesso em tempo constante, mantendo a integridade da
estrutura **LIFO (Last In, First Out)**.

------------------------------------------------------------------------

# 7. Quadro Comparativo de Arquitetura

  -----------------------------------------------------------------------
  Critério de Avaliação   Código Inicial (Gerado  Código Refatorado
                          pela IA)                (Final)
  ----------------------- ----------------------- -----------------------
  **Alocação de Memória** Dinâmica e estendida    Estática e pré-alocada
                          sob demanda (`append`,  em bloco único no
                          `realloc`, `push`).     construtor.

  **Complexidade          Variável, com           Estritamente constante
  Temporal**              possibilidade de        **O(1)** para as
                          **O(N)** devido a       operações da pilha.
                          realocações no heap/V8. 

  **Garantia de Tipagem** Heterogênea em          Rígida e uniforme
                          Python/JS ou limitada a (`array`, `union/enum`,
                          `int` em C.             `TypedArray`).

  **Tratamento do         Inexistente; aceitava   Restrito a caracteres
  `char`**                textos de qualquer      individuais de tamanho
                          tamanho.                1.

  **Tratamento de         Omisso ou com falhas    Completo, com exceções
  Exceções**              silenciosas no método   customizadas nos
                          `troca()`.              limites da estrutura.

  **Gestão de Recursos**  Risco de *Memory Leak*  Ciclo de vida
                          em C e                  controlado, desalocação
                          *De-optimization* em    segura e buffers fixos.
                          JS.                     
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 8. Lições Aprendidas

## 8.1 Abstrações de Alto Nível vs. Requisitos Físicos

Linguagens modernas como Python e JavaScript oferecem estruturas muito
flexíveis, como listas e arrays dinâmicos.

Embora facilitem a implementação inicial, essas abstrações podem violar
requisitos específicos de estruturas de dados estáticas em memória
contígua quando não são utilizadas estruturas especializadas, como
`array` e `TypedArray`.

## 8.2 Controle Determinístico O(1)

A garantia de tempo constante em estruturas estáticas depende do
desacoplamento entre a alocação de memória e a inserção dos dados.

O gerenciamento por um contador manual de quantidade permite evitar a
necessidade de realocações durante as operações da pilha.

## 8.3 Gestão Consciente de Recursos

Em linguagens de baixo nível como C, a reserva e a liberação de memória
exigem uma arquitetura rigorosa no construtor e destruidor.

Esse cuidado é fundamental para evitar comportamentos indefinidos e
vazamentos de memória.
