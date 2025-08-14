# Dados iniciais
usuarios = {}
contas = []
limite = 500
limite_saques = 3

# Funções
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f'✅ Depósito de R$ {valor:.2f} realizado com sucesso!')
    else:
        print('❌ Valor inválido! O depósito deve ser maior que zero.')
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print(f'❌ Você já realizou {limite_saques} saques hoje.')
    elif valor <= 0:
        print('❌ Valor inválido! O saque deve ser maior que zero.')
    elif valor > limite:
        print(f'❌ Valor acima do limite permitido por saque (R$ {limite:.2f}).')
    elif valor > saldo:
        print('❌ Saldo insuficiente para realizar o saque.')
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        print(f'✅ Saque de R$ {valor:.2f} realizado com sucesso!')
    return saldo, extrato

def exibir_extrato(saldo, *, extrato):
    print('\n🔍 Extrato:')
    if not extrato:
        print('Nenhuma movimentação registrada.')
    else:
        for operacao in extrato:
            print(operacao)
    print(f'Saldo atual: R$ {saldo:.2f}\n')

def cadastrar_usuario(usuarios):
    cpf = input('Digite o CPF (somente números): ')
    if cpf in usuarios:
        print('❌ Usuário já cadastrado!')
        return

    nome = input('Digite o nome completo: ')
    nascimento = input('Digite a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Digite o endereço (logradouro, número - bairro - cidade/estado): ')
    usuarios[cpf] = {
        'cpf': cpf,
        'nome': nome,
        'nascimento': nascimento,
        'endereco': endereco
    }
    print('✅ Usuário cadastrado com sucesso!')

def cadastrar_conta(contas, usuarios):
    cpf = input('Digite o CPF do usuário: ')
    usuario = usuarios.get(cpf)
    if not usuario:
        print('❌ Usuário não encontrado. Cadastre o usuário primeiro.')
        return

    numero_conta = len(contas) + 1
    conta = {
        'agencia': '0001',
        'numero_conta': numero_conta,
        'usuario': usuario,
        'saldo': 0,
        'extrato': []
    }
    contas.append(conta)
    print(f'✅ Conta criada com sucesso! Número da conta: {numero_conta}')

def encontrar_conta(contas, numero_conta):
    for conta in contas:
        if conta['numero_conta'] == numero_conta:
            return conta
    print('❌ Conta não encontrada.')
    return None

def listar_contas_do_usuario(cpf, contas):
    contas_usuario = [conta for conta in contas if conta['usuario']['cpf'] == cpf]
    if not contas_usuario:
        print('🔍 Nenhuma conta encontrada para este CPF.')
    else:
        print(f'\n📋 Contas vinculadas ao CPF {cpf}:')
        for conta in contas_usuario:
            print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']}")

# Menu principal
menu = '''
🏦 Bem-vindo ao Sistema Bancário!
Selecione uma opção:
[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Usuário
[5] Cadastrar Conta
[6] Listar contas de um usuário
[0] Sair
Digite sua opção: 
'''

while True:
    opcao = input(menu)

    if opcao in ['1', '2', '3']:
        try:
            numero_conta = int(input('Digite o número da conta: '))
        except ValueError:
            print('❌ Número de conta inválido.')
            continue

        conta = encontrar_conta(contas, numero_conta)
        if not conta:
            continue

        if opcao == '1':
            valor = float(input('Digite o valor do depósito: R$ '))
            conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'])

        elif opcao == '2':
            valor = float(input('Digite o valor do saque: R$ '))
            numero_saques = len([op for op in conta['extrato'] if "Saque" in op])
            conta['saldo'], conta['extrato'] = sacar(
                saldo=conta['saldo'],
                valor=valor,
                extrato=conta['extrato'],
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=limite_saques
            )

        elif opcao == '3':
            exibir_extrato(conta['saldo'], extrato=conta['extrato'])

    elif opcao == '4':
        cadastrar_usuario(usuarios)

    elif opcao == '5':
        cadastrar_conta(contas, usuarios)

    elif opcao == '6':
        cpf = input('Digite o CPF do usuário: ')
        listar_contas_do_usuario(cpf, contas)

    elif opcao == '0':
        print('👋 Saindo do sistema. Até logo!')
        break

    else:
        print('❌ Opção inválida! Por favor, escolha uma opção válida.')
