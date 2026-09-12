Log de Iteração e Prompts — JavaScript (Implementação Inicial)

## Prompt Enviado ao Modelo de IA
Desenvolver uma classe em JavaScript que implemente uma estrutura de dados Pilha com capacidade estática limitada. A pilha deve aceitar apenas dados de um mesmo tipo (int, float ou char), prealocar o armazenamento em memória e contar com os métodos empilha(dado), desempilha(), pilha_esta_vazia(), pilha_esta_cheia(), troca() e tamanho(), além das exceções customizadas PilhaCheiaErro, PilhaVaziaErro e TipoErro.

## Código Bruto Gerado pela IA (Versão Inicial Ineficiente)

class Pilha {
constructor(capacidade) {
this.capacidade = capacidade;
this.dados = [];
}

empilha(dado) {
    if (this.dados.length < this.capacidade) {
        this.dados.push(dado);
    } else {
        throw new PilhaCheiaErro();
    }
}

desempilha() {
    if (this.dados.length === 0) {
        throw new PilhaVaziaErro();
    }
    return this.dados.pop();
}

pilha_esta_vazia() {
    return this.dados.length === 0;
}

pilha_esta_cheia() {
    return this.dados.length === this.capacidade;
}

troca() {
    if (this.dados.length >= 2) {
        let temp = this.dados[this.dados.length - 1];
        this.dados[this.dados.length - 1] = this.dados[this.dados.length - 2];
        this.dados[this.dados.length - 2] = temp;
    }
}

tamanho() {
    return this.dados.length;
}
}