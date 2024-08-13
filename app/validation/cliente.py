from ..exceptions import ClienteException, CPFException, DataException


class Validacoes:

    @staticmethod
    def nome(nome_cliente: str):
        if not nome_cliente.strip():
            raise ClienteException("O nome do cliente não pode estar em branco")

    @staticmethod
    def cpf(cpf_cliente: str, cursor):
        if not cpf_cliente.strip() or len(cpf_cliente) != 11 or not cpf_cliente.isdigit():
            raise CPFException("CPF inválido")

        cursor.execute("SELECT cpf FROM Cliente WHERE cpf = %s", (cpf_cliente,))
        cpf_existente = cursor.fetchone()

        if cpf_existente:
            raise CPFException(f"O CPF {cpf_cliente} já está cadastrado na base de dados")

    @staticmethod
    def nascimento(data_nasc: str):
        if len(data_nasc) != 10 or data_nasc[2] != "/" or data_nasc[5] != "/":
            raise DataException("Data de nascimento inválida. O formato deve ser DD/MM/YYYY.")

    @staticmethod
    def info(outras_infos: str):
        if len(outras_infos) > 255:
            raise ClienteException("Informações adicionais são muito longas")
