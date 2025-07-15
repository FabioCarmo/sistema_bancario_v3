
# Importar modulo de identacao
import textwrap
from src.cliente import Cliente, PessoaFisica, Conta, ContaCorrente, Historico, Transacao, Saque, Deposito
from managedb.manage_dbapi import DbBanco

db = DbBanco()

def menu(clientes):

    if not clientes:

        menu = """\n
            ================ MENU ================
        [4]\tNova conta
        [6]\tLogin
        [0]\tSair
        => """
    else:
        menu = """\n
            ================ MENU ================
        [1]\tDepositar
        [2]\tSacar
        [3]\tExtrato
        [5]\tNovo usuario
        [6]\tLogin
        [7]\tExcluir meus dados
        [0]\tSair
        => """

    return input(textwrap.dedent(menu)).strip()


def filtrar_cliente(cpf):
    #clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    #return clientes_filtrados[0] if clientes_filtrados else None
    cpf = (cpf,)
    clientes_filtrados = db.listarClientes(indice=cpf)
    return clientes_filtrados if clientes_filtrados else None


def recuperar_conta_cliente(cpf):
    cpf = (cpf,)
    contas_filtradas = db.listarContas(indice=cpf)
    return contas_filtradas if contas_filtradas else None


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(cliente, conta):

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ").strip()
    cliente = filtrar_cliente(cpf)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (aaaa-mm-dd): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    dados_cliente = (nome, cpf, data_nascimento, endereco)
    resultado_db = db.inserirCliente(dados_cliente) # Metodo do db para inserir registros
    
    if resultado_db == False:
        print("Erro ao cadastrar cliente !")
        return

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = float(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cpf, numero=numero_conta)

    agencia = Conta.agencia() # Obter o numero da agencia
    dados = (cliente[0], cpf, agencia, numero_conta) # Cliente[0] armazena o id do cliente
    resultado_db = db.inserirConta(dados) # Metodo do db para inserir registros

    if resultado_db == False:
        print("Erro ao cadastrar conta !")
        return

    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def login(clientes, contas):
    cpf = float(input("Digite seu cpf: ").strip())
    cliente = filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    
    conta = recuperar_conta_cliente(cpf)
    contas.append(conta)
    clientes.append(cliente)

    print(f"Bem-vindo de volta, {cliente[1]}.")


def excluir_registro(clientes):

    if not clientes:
        print("Cliente não encontrado !")
        return 
    
    tabelas = ("clientes", "contas", "saldo", "transacao")
    dados = (tabelas, clientes[0]) # clientes[0] ID do usuario

    while True:
        opcao = input("Deseja excluir todos os seus dados ? S ou N (S para sim N para nao)").strip()

        if opcao == "S":
            dados = ("clientes", "contas", clientes[0])
            db.excluirRegistro(dados)
            if excluir_registro == False:
                print("Erro ao excluir dados !")
                return
            else:
                print("Seus dados foram excluidos com sucesso!")
                return 
            
        elif opcao == "N":
            return

        else:
            print("Opção invalida ")
            continue
        