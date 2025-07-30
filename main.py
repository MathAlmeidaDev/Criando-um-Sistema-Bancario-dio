saldo = 0
saques = []
depositos = []

menu = '''
Bem-vindo ao Sistema Bancário!
Selecione uma opção:
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
Digite sua opção: 
'''
while True:
    opcao = input(menu)
    
    if opcao == '1':
        valor = float(input('Digite o valor do depósito: R$ '))
        if valor > 0:
            depositos.append(valor)
            saldo += valor
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
        else:
            print('Valor inválido! O depósito deve ser positivo.')

    elif opcao == '2':
        if len(saques) < 3:
            valor = float(input('Digite o valor do saque: R$ '))
            if valor > 0 and valor <= 500 and valor <= saldo:
                saques.append(valor)
                saldo -= valor
                print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
            elif valor > saldo:
                print('Saldo insuficiente para realizar o saque.')
            else:
                print('Valor inválido! O saque deve ser positivo e não pode exceder R$ 500,00.')
        else:
            print('Limite de saques diários atingido. Você já realizou 3 saques hoje.')

    elif opcao == '3':
        print('\nExtrato:')
        for deposito in depositos:
            print(f'Depósito: R$ {deposito:.2f}')
        for saque in saques:
            print(f'Saque: R$ {saque:.2f}')
        print(f'Saldo atual: R$ {saldo:.2f}\n')

    elif opcao == '0':
        print('Saindo do sistema. Até logo!')
        break

    else:
        print('Opção inválida! Por favor, escolha uma opção válida.')