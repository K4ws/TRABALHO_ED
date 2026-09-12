```
Eficiência de Alocação e Garantia de Complexidade O(1)
```

```
A substituição do realloc() pela reserva do bloco contíguo completo no
criar_pilha() elimina chamadas repetidas de alocação no sistema operacional e
previne a fragmentação da memória heap. O topo passa a ser controlado
diretamente pelo ponteiro de quantidade (p->quantidade), garantindo que as
operações empilha, desempilha e troca executem em tempo estritamente constante
O(1).
```

```
Flexibilidade de Tipagem Rígida via Enum e Union
```

```
O uso combinado da enum TipoDado com a union Elemento resolve a limitação da
versão inicial de aceitar apenas inteiros. A union permite reutilizar o mesmo
espaço de memória para int, float ou char, enquanto a enum vincula o tipo
correto à pilha no momento da criação, mantendo a integridade e a segurança de
tipos do C sem estourar o limite de memória reservado.
```

```
Controle de Variações de Memória e Prevenção de Leaks
```

```
A alocação em etapa única no construtor garante determinismo ao ciclo de vida da
estrutura. A implementação da função destruir_pilha() assegura a liberação
adequada do vetor interno p->dados e da struct p, eliminando riscos de vazamento
de memória (memory leak) ou ponteiros pendentes (dangling pointers).
```

```
Tratamento Estruturado de Exceções e Segurança de Faixa (Out-of-Bounds)
As funções empilha, desempilha e troca passaram a utilizar retornos booleanos
associados à emissão das mensagens de erro padronizadas. Isso impede acessos
fora do limite alocado e previne falhas de violação de segmento (segmentation
fault) em casos de subflutuação ou transbordo de capacidade.
```

