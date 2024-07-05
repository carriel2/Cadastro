import re

from exceptions.exceptions import (
    AnoDataInvalida,
    CPFJaCadastrado,
    DataNInvalida,
    DiaInvalido,
    FormatoInfo,
    MesInvalido,
    NomeInvalido,
    TamanhoCPF, CPFException, CaracterInvalidoCPF,
)
from fastapi import HTTPException, status


def validar_nome(nome_cliente: str) -> bool:
    """
    Valida o nome do cliente.

    Parâmetros:
        nome_cliente: Nome do cliente.

    Retorna:
        - True se o nome for válido, False caso contrário.
    """
    if not re.fullmatch(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)*$', nome_cliente):
        raise NomeInvalido(
            "O nome inserido excede o limite de caracteres ou contém caracteres inválidos "
        )
    return True


def validar_cpf(cpf_cliente, cursor):
    """
    Valida o CPF do cliente e verifica se já existe no banco de dados.
    """

    cpf_cliente = re.sub(r"[^0-9]", "", cpf_cliente)

    if len(cpf_cliente) != 11:
        raise TamanhoCPF("Tamanho do CPF inválido  ")
    elif cpf_cliente.count("X") > 1 or (cpf_cliente.count("X") == 1 and cpf_cliente[-1] != "X"):
        raise CaracterInvalidoCPF("CPF deve conter apenas números ou 'X' na última posição")

    query = "SELECT 1 FROM cliente WHERE cpf = %s"
    cursor.execute(query, (cpf_cliente,))

    if cursor.fetchone():
        raise CPFException("CPF já cadastrado")

    return True


def validar_nasc(data_nasc):
    """
    Valida a data de nascimento do cliente.
    """
    data_nasc = re.sub(r"^[0-9/]$", "", data_nasc)

    if len(data_nasc) != 10 or data_nasc[2] != "/" or data_nasc[5] != "/":
        raise DataNInvalida("Formato da data inválido")

    dia, mes, ano = map(int, data_nasc.split("/"))

    if not 1899 <= ano <= 2006:
        raise AnoDataInvalida("Ano da data é maior que 2006 ou menor que 1899")

    if not 1 <= mes <= 12:
        raise MesInvalido("O mês inserido é inválido")

    if mes in [1, 3, 5, 7, 8, 10, 12]:
        if not 1 <= dia <= 31:
            raise DiaInvalido("O dia inserido é inválido")
    elif mes in [4, 6, 9, 11]:
        if not 1 <= dia <= 30:
            raise DiaInvalido("O dia inserido é inválido")
    elif mes == 2:
        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
            if not 1 <= dia <= 29:
                raise DiaInvalido("O dia inserido é inválido")
        else:
            if not 1 <= dia <= 28:
                raise DiaInvalido("O dia inserido é inválido")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Data inválida"
        )

    return True


def validar_info(outras_infos):
    """
    Valida as informações adicionais do cliente.
    """
    if len(outras_infos) > 30:
        raise FormatoInfo(
            "Informações adicionais não pode conter mais do que 30 caracteres"
        )

    return True
