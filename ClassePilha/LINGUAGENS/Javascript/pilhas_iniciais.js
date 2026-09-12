// Exceções customizadas exigidas
class PilhaCheiaErro extends Error {
    constructor(message = "A pilha está cheia.") {
        super(message);
        this.name = "PilhaCheiaErro";
    }
}

class PilhaVaziaErro extends Error {
    constructor(message = "A pilha está vazia.") {
        super(message);
        this.name = "PilhaVaziaErro";
    }
}

class TipoErro extends Error {
    constructor(message = "Tipo de dado incompatível.") {
        super(message);
        this.name = "TipoErro";
    }
}

// Implementação Inicial da IA (com falhas de arquitetura)
class Pilha {
    constructor(capacidade) {
        this.capacidade = capacidade;
        this.dados = []; // FALHA: Uso de Array dinâmico heterogêneo em vez de TypedArray
    }

    empilha(dado) {
        if (this.dados.length >= this.capacidade) {
            throw new PilhaCheiaErro();
        }
        this.dados.push(dado); // FALHA: Crescimento dinâmico e realocação no heap
    }

    desempilha() {
        if (this.pilha_esta_vazia()) {
            throw new PilhaVaziaErro();
        }
        return this.dados.pop(); // FALHA: Redimensionamento físico em tempo de execução
    }

    pilha_esta_vazia() {
        return this.dados.length === 0;
    }

    pilha_esta_cheia() {
        return this.dados.length === this.capacidade;
    }

    troca() {
        if (this.dados.length >= 2) {
            let topo = this.dados.length - 1;
            let abaixo = this.dados.length - 2;
            let temp = this.dados[topo];
            this.dados[topo] = this.dados[abaixo];
            this.dados[abaixo] = temp;
        }
    }

    tamanho() {
        return this.dados.length;
    }
}

// --- TESTE DA IMPLEMENTAÇÃO INICIAL ---
console.log("--- Executando Teste Inicial da Pilha (JavaScript) ---");

const pilha = new Pilha(3);

// Empilhando dados no array dinâmico
pilha.empilha(10);
pilha.empilha("TextoIncompativel"); // FALHA: Aceita misturar tipos na mesma instância
pilha.empilha(30);

console.log("Dados da pilha:", pilha.dados);
console.log("Tamanho atual:", pilha.tamanho());
console.log("Está cheia?:", pilha.pilha_esta_cheia());
console.log("Elemento removido:", pilha.desempilha());
console.log("Tamanho após remoção:", pilha.tamanho());



// --- BATERIA DE TESTES DA IMPLEMENTAÇÃO INICIAL (JAVASCRIPT) ---
// Este teste evidencia as falhas de arquitetura do código inicial gerado pela IA.

console.log("==================================================");
console.log("   EXECUTANDO TESTES DA IMPLEMENTAÇÃO INICIAL (JS) ");
console.log("==================================================\n");

const pilhaInicial = new Pilha(3);

// 1. Falha de Tipagem: Aceitação de Dados Heterogêneos
console.log("[FALHA 1] Injeção de tipos mistos na mesma pilha...");
pilhaInicial.empilha(10);                    // Número Inteiro
pilhaInicial.empilha("TextoMuitoLongo");      // String Longa (deveria aceitar apenas char de tamanho 1)
pilhaInicial.empilha(45.67);                 // Número Float

console.log("  ✗ Estado da pilha (dados misturados):", pilhaInicial.dados);
console.log("  ✗ PROBLEMA: A pilha aceitou dados heterogêneos sem disparar TipoErro.\n");

// 2. Falha de Armazenamento: Uso de Redimensionamento Dinâmico
console.log("[FALHA 2] Verificação de redimensionamento dinâmico...");
console.log("  ✗ Tamanho do Array nativo:", pilhaInicial.dados.length);
console.log("  ✗ PROBLEMA: O tamanho do Array cresceu via push() em vez de ser pré-alocado no construtor.\n");

// 3. Remoção de Elementos via pop()
console.log("[FALHA 3] Remoção de elemento do topo...");
let removido = pilhaInicial.desempilha();
console.log("  ✗ Elemento removido via pop():", removido);
console.log("  ✗ Novo tamanho da pilha:", pilhaInicial.tamanho());
console.log("  ✗ PROBLEMA: O método desempilha() alterou fisicamente a estrutura do vetor no heap.\n");

// 4. Falha Silenciosa no Método troca()
console.log("[FALHA 4] Teste da operação troca() com elementos insuficientes...");
const pilhaPequena = new Pilha(3);
pilhaPequena.empilha('A'); // Apens 1 elemento inserido

try {
    pilhaPequena.troca(); // Deveria disparar PilhaVaziaErro
    console.log("  ✗ A operação troca() executou sem erros.");
    console.log("  ✗ PROBLEMA: O método falhou silenciosamente sem disparar a exceção PilhaVaziaErro.\n");
} catch (e) {
    console.log("  ✓ Exceção lançada corretamente:", e.message);
}

console.log("==================================================");
console.log("   FIM DOS TESTES DA IMPLEMENTAÇÃO INICIAL        ");
console.log("==================================================");