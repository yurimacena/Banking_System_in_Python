menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

==> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    option = input(menu)

    if option == "d":
        print("----------Depósito----------")
        value = float(input("Escreva o valor do depósito: "))

        if value > 0:
            saldo += value
            extrato += f"Depósito: R$ {value: .2f}\n"

        else:
            print("Erro na operação. O valor submetido é inválido!")

    elif option == "s":
        print("----------Saque----------")
        value = float(input("Escreva o valor do saque: "))

        excedeu_saldo = value > saldo

        excedeu_limite = value > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Erro na operação. Você não tem saldo suficiente!")

        elif excedeu_limite:
            print("Erro na operação. O valor do saque excedeu o limite!")

        elif excedeu_saques:
            print("Erro na operação. Número máximo de saques excedido!")

        elif value > 0:
            saldo -= value
            extrato += f"Saque: R$ {value: .2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso.")

        else:
            print("Erro na operação. O valor informado é inválido.")

    elif option == "e":
        print("----------Extrato----------")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("---------------------------")

    elif option == "q":
        break

    else:
        print("Erro na operação, por favor selecione novamente a operação deseja.")