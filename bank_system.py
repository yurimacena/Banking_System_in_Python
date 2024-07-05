from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

def menu():
    menu = """\n
    MENU
    [1]Depositar
    [2]Sacar
    [3]Extrato
    [4]Nova conta
    [5]Listar contas
    [6]Novo usuário
    [0]Sair
    -> """
    return input(menu)

class AccountsInteractor:
    def __init__ (self, accounts):
        self.accounts = accounts
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            account = self.accounts[self._index]
            return f"""
            Agência:\t{account.agencia}
            Número:\t{account.numero}
            Titular:\t{account.cliente.nome}
            Saldo:\tR$ {account.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.accounts = []
        self.index_account = 0

    def realizar_transacao(self, account, transaction):
        if len(account.historico.day_transactions()) >= 2:
            print("\nFoi excedida o número de transações permitidas para hoje.")
            return

        transaction.registrar(account)

    def adicionar_conta(self, account):
        self.accounts.append(account)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def new_account(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)
        
    def sacar(self, valor):
        numero_saques = len(
            [transaction 
                for transaction in self.historico._transactions 
                if transaction["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transactions = []

    @property
    def transacoes(self):
        return self._transactions

    def adicionar_transacao(self, transaction):
        self._transactions.append(
            {
                "tipo": transaction.__class__.__name__,
                "valor": transaction.valor,
                "data": datetime.now().strftime( "%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, transaction_type=None):
        for transaction in self._transactions:
            if transaction_type is None or transaction["tipo"].lower() == transaction_type.lower():
                yield transaction

    def day_transactions(self):
        actual_date = datetime.utcnow().date()
        transactions = []

        for transaction in self._transactions:
            transaction_date = datetime.strptime(transaction["data"], "%d-%m-%Y %H:%M:%S").date()
            if actual_date == transaction_date:
                transactions.append(transaction)
        return transactions

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, account):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, account):
        sucesso_transacao = account.sacar(self.valor)

        if sucesso_transacao:
            account.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, account):
        sucesso_transacao = account.depositar(self.valor)

        if sucesso_transacao:
            account.historico.adicionar_transacao(self)


def transaction_log(func):
    def envelope(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return result
    return envelope


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.accounts:
        print("\nCliente não possui conta!")
        return
    return cliente.accounts[0]


@transaction_log
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transaction = Deposito(valor)

    account = recuperar_conta_cliente(cliente)
    if not account:
        return

    cliente.realizar_transacao(account, transaction)


@transaction_log
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transaction = Saque(valor)

    account = recuperar_conta_cliente(cliente)
    if not account:
        return

    cliente.realizar_transacao(account, transaction)


@transaction_log
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    account = recuperar_conta_cliente(cliente)
    if not account:
        return

    print("\nEXTRATO")
    extract = ""
    have_transaction = False
    for transaction in account.historico.gerar_relatorio():
        have_transaction = True
        extract += f"\n{transaction["tipo"]}: R$ {transaction["valor"]:.2f}"
    if not have_transaction:
        extract = "Não foram realizadas movimentações."

    print(extract)
    print(f"\nSaldo:\n\tR$ {account.saldo:.2f}")
    print()


@transaction_log
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")


@transaction_log
def criar_conta(numero_conta, clientes, accounts):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    account = ContaCorrente.new_account(cliente=cliente, numero=numero_conta, limite=500, limite_saques=50)
    accounts.append(account)
    cliente.accounts.append(account)

    print("\nConta criada com sucesso!")


def listar_contas(accounts):
    for account in AccountsInteractor(accounts):
        print()
        print(str(account))


def main():
    clientes = []
    accounts = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "4":
            numero_conta = len(accounts) + 1
            criar_conta(numero_conta, clientes, accounts)

        elif opcao == "5":
            listar_contas(accounts)

        elif opcao == "0":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")
main()