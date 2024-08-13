from app.exceptions import CPFException, ClienteException
from app.validation.cliente import Validacoes
from app.dtos import ClienteDTO, AtualizaClienteDTO


class ClienteService:

    @staticmethod
    def create_cliente(body: ClienteDTO, cursor):
        nome_cliente = body.nome
        cpf_cliente = body.cpf
        data_nasc = body.data_nasc
        inf_adc = body.inf_adicionais

        Validacoes.nome(nome_cliente)
        Validacoes.cpf(cpf_cliente, cursor)
        Validacoes.nascimento(data_nasc)

        if inf_adc is not None:
            Validacoes.info(inf_adc)

        cursor.execute("""
            INSERT INTO Cliente (nome, cpf, data_nasc, info_adicional)
            VALUES (%s, %s, %s, %s)
       """, (nome_cliente, cpf_cliente, data_nasc, inf_adc))

    @staticmethod
    def consulta_clientes(cursor):
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        if not clientes:
            raise ClienteException("Nenhum cliente encontrado na base de dados")

        return [
            {
                'id': cliente[0],
                'nome': cliente[1],
                'data_nasc': cliente[2],
                'info_adicional': cliente[3],
                'cpf': cliente[4],
            }
            for cliente in clientes
        ]

    @staticmethod
    def consulta_cliente_cpf(cpf: str, cursor):
        cursor.execute("SELECT * FROM Cliente WHERE cpf = %s", (cpf,))
        cliente_info = cursor.fetchone()

        if not cliente_info:
            raise ClienteException("Cliente não encontrado")

        return {
            'id': cliente_info[0],
            'nome': cliente_info[1],
            'data_nasc': cliente_info[2],
            'info_adicional': cliente_info[3],
            'cpf': cliente_info[4],
        }

    @staticmethod
    def atualizar_cliente(id: str, body: AtualizaClienteDTO, cursor):
        nome = body.nome
        data_nasc = body.data_nasc
        inf_adicionais = body.inf_adicionais

        Validacoes.nome(nome_cliente=nome)
        Validacoes.nascimento(data_nasc=data_nasc)
        Validacoes.info(outras_infos=inf_adicionais)

        cursor.execute("""
            UPDATE cliente
            SET nome=%s, data_nasc=%s, info_adicional=%s
            WHERE id=%s
        """, (nome, data_nasc, inf_adicionais, id))

    @staticmethod
    def deleta_cliente(cpf: str, cursor):
        cursor.execute("DELETE FROM Cliente WHERE cpf = %s", (cpf,))
        if cursor.rowcount == 0:
            raise CPFException(f"CPF {cpf} não encontrado")
