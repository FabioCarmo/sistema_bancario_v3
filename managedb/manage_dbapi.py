
# Importar base de dados sqlite
import sqlite3
from pathlib import Path

# Classe DbBanco para realizar operacoes na base de dados

class DbBanco:

    def __init__(self):
        self._PATH = Path(__file__).parent # Diretorio raiz do projeto
        self._enderecodb = f"{self._PATH}\db_bancodasnotas.db" # Caminho do arquivo db
        self._conexao = sqlite3.connect(self._enderecodb)
        self._cursor = self._conexao.cursor()

    # Status de conexao retorn True para sucesso ou codigo de erro para falhas
    def status(self):
        try:
            self._conexao()
            return True
        except ValueError as exc:
            return exc

    # Criar as tabelas 'clientes' e 'contas' com suas colunas e atributos
    def criar_tabela(self):
        self._cursor.execute("CREATE TABLE clientes (ID INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(50), cpf float (11), data_nascimento DATE, endereco VARCHAR)")
        self._cursor.execute("CREATE TABLE contas(ID INTEGER, cpf FLOAT(11) UNIQUE, agencia INTEGER(6) UNIQUE NOT NULL, conta INTEGER(9) UNIQUE NOT NULL)")
        self._conexao.commit()
    
    # Inserir registros na tabela 'clientes'
    def inserirCliente(self, dados):
        try:
            self._cursor.execute("INSERT INTO clientes(nome, cpf, data_nascimento, endereco) VALUES(?,?,?,?)", dados)
            self._conexao.commit()
            return True
        except:
            # Evitar registro acidental e voltar pro inicio
            self._conexao.rollback()
            return False
    
    # inserir registros na tabela 'contas'
    def inserirConta(self, dados):
        try:
            self._cursor.execute("INSERT INTO contas(ID, cpf, agencia, conta) VALUES(?,?,?,?)", dados)
            self._conexao.commit()
            return True
        except:
            # Evitar registro acidental e voltar pro inicio
            self._conexao.rollback()
            return False
    
    # Retornar os dados da tabela clientes
    def listarClientes(self, indice = False):
        if (indice == False):
            self._cursor.execute("SELECT * FROM clientes;")
            return self._cursor.fetchall()
        else:
            self._cursor.execute("SELECT * FROM clientes WHERE cpf = ?;", indice)
            return self._cursor.fetchone()

    # Retornar os dados da contas
    def listarContas(self, indice=False):
        if (indice == False):
            self._cursor.execute("SELECT * FROM contas;")
            return self._cursor.fetchall()
        else:
            self._cursor.execute("SELECT * FROM contas WHERE ID = ?;", indice)
            return self._cursor.fetchone()
        

    def atualizarCliente(self, tipo):
        pass
    
    # Excluir registro por chave primaria
    def excluirRegistro(self, dados):
        try:
            tabela, id_valor = dados
            if tabela not in ("clientes", "contas"):
                raise ValueError("Tabela inválida")
            self._cursor.execute(f"DELETE FROM {tabela} WHERE ID = ?", (id_valor,))
            self._conexao.commit()
        except ValueError:
            self._conexao.rollback()
            return False
    
    # Encerra a conexao com a base de dados
    def fechar(self):
        if (self.status()):
            self._conexao.close()