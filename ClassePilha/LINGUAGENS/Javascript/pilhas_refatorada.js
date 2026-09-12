// Exceções Customizadas exigidas pelo enunciado
class PilhaCheiaErro extends Error {
    constructor(message = "PilhaCheiaErro: A pilha está cheia.") {
        super(message);
        this.name = "PilhaCheiaErro";
    }
}

class PilhaVaziaErro extends Error {
    constructor(message = "PilhaVaziaErro: A pilha está vazia.") {
        super(message);
        this.name = "PilhaVaziaErro";
    }
}

class TipoErro extends Error {
    constructor(message = "TipoErro: Tipo de dado incompatível.") {
        super(message);
        this.name = "TipoErro";
    }
}

// Classe Pilha com Alocação Física Contígua via TypedArray
class Pilha {
    constructor(capacidade, tipo) {
        if (capacidade <= 0) {
            throw new Error("A capacidade deve ser maior que zero.");
        }

        this.capacidade = capacidade;
        this.tipo = tipo;
        this.quantidade = 0; // Ponteiro manual de quantidade (topo)

        // Instanciação física do TypedArray com bloco contíguo de memória
        if (tipo === Number || tipo === 'int') {
            this.dados = new Int32Array(capacidade);
        } else if (tipo === 'float') {
            this.dados = new Float64Array(capacidade);
        } else if (tipo === String || tipo === 'char') {
            this.dados = new Uint16Array(capacidade); // Armazena UTF-16 code units
        } else {
            throw new TipoErro("Tipo não suportado. Use 'int', 'float' ou 'char'.");
        }
    }

    empilha(dado) {
        if (this.pilha_esta_cheia()) {
            throw new PilhaCheiaErro();
        }

        // Validação estrita do tipo de dado
        if (this.tipo === String || this.tipo === 'char') {
            if (typeof dado !== 'string' || dado.length !== 1) {
                throw new TipoErro("O dado deve ser um único caractere (string de tamanho 1).");
            }
            this.dados[this.quantidade] = dado.charCodeAt(0);
        } else if (this.tipo === Number || this.tipo === 'int' || this.tipo === 'float') {
            if (typeof dado !== 'number' || isNaN(dado)) {
                throw new TipoErro("O dado deve ser um número válido.");
            }
            this.dados[this.quantidade] = dado;
        } else {
            throw new TipoErro();
        }

        this.quantidade++;
    }

    desempilha() {
        if (this.pilha_esta_vazia()) {
            throw new PilhaVaziaErro();
        }

        this.quantidade--;
        let valor = this.dados[this.quantidade];

        if (this.tipo === String || this.tipo === 'char') {
            return String.fromCharCode(valor);
        }
        return valor;
    }

    pilha_esta_vazia() {
        return this.quantidade === 0;
    }

    pilha_esta_cheia() {
        return this.quantidade === this.capacidade;
    }

    troca() {
        if (this.quantidade < 2) {
            throw new PilhaVaziaErro("PilhaVaziaErro: É necessário ter pelo menos 2 elementos para trocar.");
        }

        let topo = this.quantidade - 1;
        let abaixo = this.quantidade - 2;

        let temp = this.dados[topo];
        this.dados[topo] = this.dados[abaixo];
        this.dados[abaixo] = temp;
    }

    tamanho() {
        return this.quantidade;
    }
}

// --- BATERIA DE TESTES AUTOMATIZADOS E ESTRESSE ---
console.log("==================================================");
console.log("   INICIANDO BATERIA DE TESTES DA PILHA (JS)      ");
console.log("==================================================\n");

// 1. Teste de Operações Básicas (Inteiros)
console.log("[TESTE 1] Operações Básicas com Inteiros...");
const pInt = new Pilha(3, 'int');
console.assert(pInt.pilha_esta_vazia() === true, "Erro no teste de pilha vazia");

pInt.empilha(10);
pInt.empilha(20);
pInt.empilha(30);

console.assert(pInt.tamanho() === 3, "Erro no tamanho");
console.assert(pInt.pilha_esta_cheia() === true, "Erro no teste de pilha cheia");

let removido = pInt.desempilha();
console.assert(removido === 30, "Erro ao desempilhar LIFO");
console.log(`  ✓ Elemento desempilhado: ${removido}`);

pInt.troca();
removido = pInt.desempilha();
console.assert(removido === 10, "Erro após operação troca()");
console.log(`  ✓ Elemento desempilhado após troca(): ${removido}`);
console.log("  [PASS] Teste 1 concluído com sucesso!\n");

// 2. Estresse: Overflow (PilhaCheiaErro)
console.log("[TESTE 2] Cenário de Estresse: Pilha Cheia (Overflow)...");
const pCheia = new Pilha(2, 'int');
pCheia.empilha(100);
pCheia.empilha(200);

try {
    pCheia.empilha(300);
    console.assert(false, "Erro: Não lançou PilhaCheiaErro");
} catch (e) {
    console.assert(e instanceof PilhaCheiaErro, "Exceção incorreta");
    console.log(`  ✓ Exceção capturada com sucesso: ${e.message}`);
    console.log("  [PASS] Teste 2 (Overflow) concluído com sucesso!\n");
}

// 3. Estresse: Underflow (PilhaVaziaErro)
console.log("[TESTE 3] Cenário de Estresse: Pilha Vazia (Underflow)...");
const pVazia = new Pilha(3, 'int');

try {
    pVazia.desempilha();
    console.assert(false, "Erro: Não lançou PilhaVaziaErro ao desempilhar");
} catch (e) {
    console.assert(e instanceof PilhaVaziaErro, "Exceção incorreta");
    console.log(`  ✓ Exceção ao desempilhar capturada: ${e.message}`);
}

try {
    pVazia.troca();
    console.assert(false, "Erro: Não lançou PilhaVaziaErro ao trocar");
} catch (e) {
    console.assert(e instanceof PilhaVaziaErro, "Exceção incorreta");
    console.log(`  ✓ Exceção no método troca() capturada: ${e.message}`);
    console.log("  [PASS] Teste 3 (Underflow) concluído com sucesso!\n");
}

// 4. Estresse: Tipo Incompatível (TipoErro)
console.log("[TESTE 4] Cenário de Estresse: Tipo Incompatível...");
const pTipo = new Pilha(3, 'int');

try {
    pTipo.empilha("TextoInvalido");
    console.assert(false, "Erro: Permitiu inserir string em pilha de int");
} catch (e) {
    console.assert(e instanceof TipoErro, "Exceção incorreta");
    console.log(`  ✓ Exceção TipoErro capturada: ${e.message}`);
    console.log("  [PASS] Teste 4 (TipoIncompativel) concluído com sucesso!\n");
}

// 5. Teste com Caractere (char)
console.log("[TESTE 5] Operações com Caractere (char)...");
const pChar = new Pilha(2, 'char');
pChar.empilha('A');
pChar.empilha('B');

let charRemovido = pChar.desempilha();
console.assert(charRemovido === 'B', "Erro no desempilhar de char");
console.log(`  ✓ Caractere desempilhado do Uint16Array: ${charRemovido}`);
console.log("  [PASS] Teste 5 (char) concluído com sucesso!\n");

console.log("==================================================");
console.log("   TODOS OS TESTES EM JS FORAM EXECUTADOS COM SUCESSO!");
console.log("==================================================");