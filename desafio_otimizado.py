menu = """===============MENU===============

    \t[u] Criar usuário
    \t[c] Criar conta corrente
    \t[l] Listar contas
    \t[d] Depositar
    \t[s] Sacar
    \t[e] Extrato
    \t[q] Sair
==================================\nTecle uma das letras para continuar:\n"""
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    option = input(menu)

    def criar_user(usuarios):
        cpf = input("Informe o CPF (somente número): ")
        usuario = filtrar_usuario(cpf, usuarios)
        
        if usuario:
            print("Foi detectada uma conta existente com este CPF!")
            return
        
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})

    print("Usuário criado com sucesso!")

    def criar_conta():
        print()

    def listar_contas(contas):
        for conta in contas:
            linha = f"""\
                Agência:\t{conta[agencia]}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 1000)
            print(linha)

    def saque(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
        print("----------Saque----------")
        valor = float(input("Escreva o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Erro na operação. Você não tem saldo suficiente!")

        elif excedeu_limite:
            print("Erro na operação. O valor do saque excedeu o limite!")

        elif excedeu_saques:
            print("Erro na operação. Número máximo de saques excedido!")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor: .2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso.")

        else:
            print("Erro na operação. O valor informado é inválido.")


    def deposito(saldo, valor, extrato, /):
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: \tR$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Erro na operação. O valor informado é inválido!")

        return saldo, extrato
    
    def extrato():
        print("----------Extrato----------")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("---------------------------")