from abc import ABC, abstractmethod

# Classe que registra o histórico de transações de uma conta
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Interface base para qualquer tipo de transação
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe que representa um depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta._alterar_saldo(self.valor)
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
            print(f"✅ Depósito de R$ {self.valor:.2f} realizado com sucesso!")
        else:
            print("❌ Valor inválido! O depósito deve ser maior que zero.")

# Classe que representa um saque
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        numero_saques = len([t for t in conta.historico.transacoes if "Saque" in t])
        if numero_saques >= conta.limite_saques:
            print(f"❌ Você já realizou {conta.limite_saques} saques hoje.")
        elif self.valor <= 0:
            print("❌ Valor inválido! O saque deve ser maior que zero.")
        elif self.valor > conta.limite:
            print(f"❌ Valor acima do limite permitido por saque (R$ {conta.limite:.2f}).")
        elif self.valor > conta.saldo:
            print("❌ Saldo insuficiente para realizar o saque.")
        else:
            conta._alterar_saldo(-self.valor)
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
            print(f"✅ Saque de R$ {self.valor:.2f} realizado com sucesso!")

# Classe base para clientes
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Cliente pessoa física, herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Classe base para contas bancárias
class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self.numero = numero
        self.cliente = cliente
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def _alterar_saldo(self, valor):
        self._saldo += valor

# Conta corrente com limites específicos, herda de Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

# "Banco de dados" em memória
clientes = {}  # Dicionário de clientes por CPF
contas = []    # Lista de todas as contas criadas

# Função para buscar uma conta pelo número
def encontrar_conta(numero):
    for conta in contas:
        if conta.numero == numero:
            return conta
    print("❌ Conta não encontrada.")
    return None

# Função para exibir o extrato de uma conta
def exibir_extrato(conta):
    print("\n🔍 Extrato:")
    if not conta.historico.transacoes:
        print("Nenhuma movimentação registrada.")
    else:
        for transacao in conta.historico.transacoes:
            print(transacao)
    print(f"Saldo atual: R$ {conta.saldo:.2f}\n")

# Função para listar todas as contas de um cliente
def listar_contas_do_cliente(cpf):
    cliente = clientes.get(cpf)
    if not cliente:
        print("❌ Cliente não encontrado.")
        return
    if not cliente.contas:
        print("🔍 Nenhuma conta vinculada a este CPF.")
        return
    print(f"\n📋 Contas do cliente {cliente.nome}:")
    for conta in cliente.contas:
        print(f"Agência: 0001 | Conta: {conta.numero}")

# Menu principal do sistema
menu = '''
🏦 Bem-vindo ao Sistema Bancário OO!
Selecione uma opção:
[1] Cadastrar Cliente
[2] Criar Conta Corrente
[3] Depositar
[4] Sacar
[5] Extrato
[6] Listar Contas por CPF
[0] Sair
Digite sua opção: 
'''

# Loop principal do sistema
while True:
    opcao = input(menu)

    if opcao == '1':
        # Cadastro de cliente
        cpf = input("CPF: ")
        if cpf in clientes:
            print("❌ Cliente já cadastrado.")
            continue
        nome = input("Nome: ")
        nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        endereco = input("Endereço: ")
        cliente = PessoaFisica(cpf, nome, nascimento, endereco)
        clientes[cpf] = cliente
        print("✅ Cliente cadastrado com sucesso!")

    elif opcao == '2':
        # Criação de conta corrente
        cpf = input("CPF do cliente: ")
        cliente = clientes.get(cpf)
        if not cliente:
            print("❌ Cliente não encontrado.")
            continue
        numero_conta = len(contas) + 1
        conta = ContaCorrente(cliente, numero_conta)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        print(f"✅ Conta criada com sucesso! Número: {numero_conta}")

    elif opcao == '3':
        # Realizar depósito
        try:
            numero = int(input("Número da conta: "))
            valor = float(input("Valor do depósito: R$ "))
        except ValueError:
            print("❌ Entrada inválida.")
            continue
        conta = encontrar_conta(numero)
        if conta:
            deposito = Deposito(valor)
            conta.cliente.realizar_transacao(conta, deposito)

    elif opcao == '4':
        # Realizar saque
        try:
            numero = int(input("Número da conta: "))
            valor = float(input("Valor do saque: R$ "))
        except ValueError:
            print("❌ Entrada inválida.")
            continue
        conta = encontrar_conta(numero)
        if conta:
            saque = Saque(valor)
            conta.cliente.realizar_transacao(conta, saque)

    elif opcao == '5':
        # Exibir extrato
        try:
            numero = int(input("Número da conta: "))
        except ValueError:
            print("❌ Entrada inválida.")
            continue
        conta = encontrar_conta(numero)
        if conta:
            exibir_extrato(conta)

    elif opcao == '6':
        # Listar contas por CPF
        cpf = input("CPF do cliente: ")
        listar_contas_do_cliente(cpf)

    elif opcao == '0':
        # Encerrar o sistema
        print("👋 Saindo do sistema. Até logo!")
        break

    else:
        print("❌ Opção inválida.")
