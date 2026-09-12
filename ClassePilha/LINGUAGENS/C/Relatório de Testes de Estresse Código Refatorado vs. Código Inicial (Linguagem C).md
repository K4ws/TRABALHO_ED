Este relatório apresenta o confronto direto entre a versão inicial do código em C e a versão refatorada, demonstrando como a refatoração supera a implementação ingênua em estabilidade, gerenciamento de memória e proteção contra falhas em tempo de execução.

Teste de Estresse: Transbordo de Capacidade (Overflow)

Código Inicial: Utilizava a função realloc() a cada inserção. Em vez de respeitar o limite fixo, a estrutura continuava alocando novos blocos de memória no heap indefinidamente.

Código Refatorado: Pré-aloca o bloco contíguo total (capacidade * sizeof(Elemento)) na inicialização. Ao atingir a capacidade máxima, o ponteiro p->quantidade bloqueia a escrita e dispara a mensagem "PilhaCheiaErro", mantendo o limite do vetor intacto.

Resultado: O código refatorado garante a capacidade estática requerida e previne o consumo descontrolado de memória no heap.

Teste de Estresse: Subflutuação e Acesso Fora da Faixa (Underflow & Out-of-Bounds)

Código Inicial: Ao tentar desempilhar em uma pilha vazia ou executar a troca sem elementos suficientes, o código tentava acessar índices inválidos na memória ou retornava o valor -1 (que podia ser confundido com um inteiro válido).

Código Refatorado: A função desempilha() e a função troca() verificam se p->quantidade atende aos requisitos mínimos (1 e 2 elementos, respectivamente) antes de manipular os ponteiros. Caso não atenda, retornam false e disparam "PilhaVaziaErro".

Resultado: O código refatorado impede completamente erros de Segmentation Fault e evita o vazamento de valores lixo do sistema.

Teste de Estresse: Estabilidade de Memória e Prevenção de Memory Leaks

Código Inicial: Definia o ponteiro de dados como NULL na criação e dependia do realloc() a cada inclusão. Caso o realloc() falhasse no meio do processo, o ponteiro original era perdido, gerando vazamento de memória (memory leak).

Código Refatorado: A alocação ocorre em etapa única no construtor e a desalocação é centralizada na função destruir_pilha(), que libera o vetor interno p->dados e o ponteiro p.

Resultado: O código refatorado garante o ciclo de vida seguro da memória, eliminando riscos de vazamentos ou ponteiros pendentes (dangling pointers).

Teste de Estresse: Desempenho e Complexidade O(1)

Código Inicial: A reordenação frequente de memória pelo realloc() exigia que o sistema operacional buscasse e copiasse blocos contíguos no heap, degradando a complexidade temporal das operações.

Código Refatorado: Como o espaço de memória física está reservado desde o início, a inserção, a remoção e a troca ocorrem via manipulação direta de índices do vetor, operando em tempo estritamente constante O(1).

Resultado: O código refatorado elimina a variação de tempo de execução e garante alta performance previsível.