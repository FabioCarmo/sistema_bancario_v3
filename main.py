# Um sistema bancario para deposito, saque e extrato
# Crie uma conta vincule essa conta a um usuario
# Seguindo o paradigma de POO
# Agora tornando o sistema mais legivel e garantindo mais
# Perfomance e manutenabilidade
# Integrado com a base de dados usando o python DB API (Db atual SQLite3)
# Desafio DIO Back-End Python santander 2025
# Autor: Fábio Gonçalves
# Data: 22-06-2025 Versão: 4.0

from time import sleep

# importar modulos do projeto
from src.options import menu, depositar, sacar, exibir_extrato,  filtrar_cliente, criar_cliente, criar_conta, \
listar_contas, recuperar_conta_cliente

# Funcao principal do sistema
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)
            sleep(1)
        elif opcao == "2":
            sacar(clientes)
            sleep(1)

        elif opcao == "3":
            exibir_extrato(clientes)
            sleep(3)

        elif opcao == "4":
            criar_cliente(clientes)
            sleep(1)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            sleep(1)

        elif opcao == "6":
            listar_contas(contas)
            sleep(1)

        elif opcao == "0":
            print("Encerrando..")
            sleep(2)
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Iniciar funcao main
if __name__ ==  "__main__":
    main()