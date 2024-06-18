menu = """================MENU================
    \t[u] Criar usuário
    \t[c] Criar conta corrente
    \t[l] Listar contas
    \t[d] Depositar
    \t[s] Sacar
    \t[e] Extrato
    \t[q] Sair
\nTecle uma das letras para continuar:\n"""

def criar_user(usuarios):
    print("----------Criar usuários----------")
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
        
    if usuario:
        print("Foi detectada uma conta existente com este CPF!")
        return
        
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})
    print()

    print("Usuário criado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    print("----------Criar conta corrente----------")
    cpf = input("Escreva o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta realizada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    else:
        print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    print("----------Saque----------")

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Erro na operação. Você não tem saldo suficiente!")

    elif excedeu_limite:
        print("Erro na operação. O valor do saque excedeu o limite!")

    elif excedeu_saques:
        print("Erro na operação. Número máximo de saques excedido!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")

    else:
       print("Erro na operação. O valor informado é inválido.")

    return saldo, extrato

def deposito(saldo, valor, extrato, /):
    print("----------Depósito----------").upper()
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print()
        print("Depósito realizado com sucesso!")
    else:
        print()
        print("Erro na operação. O valor informado é inválido!")

    return saldo, extrato
    
def extrato(saldo, /, *, extrato):
    print("----------Extrato----------")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")

def home():

    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    contador_de_contas = 1

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            extrato(saldo, extrato=extrato)

        elif opcao == "u":
            criar_user(usuarios)

        elif opcao == "c":
            conta = criar_conta(AGENCIA, contador_de_contas, usuarios)

            if conta:
                contas.append(conta)
                contador_de_contas += 1

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
home()