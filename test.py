# armazenas chave-valor

menu = """

[u] Criar usuário
[c] Criar conta corrente
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

    def criar_user():
        print()

    def criar_conta():
        print()

    def saque():
        print("Saque")
        return saldo and extrato

    def deposito():
        print("Depósito")
        return saldo and extrato
    
    def extrato():
        print("Extrato")