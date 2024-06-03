import os.path
import re

from exceptions.exceptions import (
    AnoDataInvalida,
    CPFJaCadastrado,
    DataNInvalida,
    DiaInvalido,
    FormatoInfo,
    MesInvalido,
    NomeInvalido,
    TamanhoCPF,
)
from fastapi import HTTPException, status


def verificar_arquivo(nome_arquivo):
    """
    Verifica se o arquivo existe e escreve o cabeçalho se necessário.
    """
    diretorio = "arquivos_cadastro"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    if not os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, "w") as arquivo:
            arquivo.write("CADASTRO CLIENTE\n")


def adicionar_informacoes_arquivo_2(
    nome_arquivo, id_cliente, nome_cliente, cpf_cliente, data_nasc, infos_adc
):
    """
    Adiciona as informações ao arquivo.
    """
    with open(nome_arquivo, "a") as arquivo:
        id_formatado = id_cliente.zfill(10)
        nome_formatado = nome_cliente.ljust(40)
        data_formatada = data_nasc.replace("/", "")
        informacoes = (
            f"{id_formatado}{nome_formatado}{cpf_cliente}{data_formatada}{infos_adc}"
        )
        arquivo.write(f"{informacoes}\n")


def cadastro_cliente_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variaveis que devem ser armazenadas
    na ordem correta.
    """
    verificar_arquivo("cadastro_cliente.txt")

    id_cliente = proximo_id()
    nome_cliente = validar_nome()
    cpf_cliente = validar_cpf()
    data_nasc = validar_nasc()
    infos_adc = validar_info()

    adicionar_informacoes_arquivo_2(
        "arquivos_cadastro/cadastro_cliente.txt",
        id_cliente,
        nome_cliente,
        cpf_cliente,
        data_nasc,
        infos_adc,
    )


def validar_nome(nome_cliente: str) -> bool:
    """
    Valida o nome do cliente.

    Parâmetros:
        nome_cliente: Nome do cliente.

    Retorna:
        - True se o nome for válido, False caso contrário.
    """
    if len(nome_cliente) > 40 or " " in nome_cliente:
        raise NomeInvalido(
            "O nome inserido excede o limite de caracteres ou contém espaços "
        )
    return True


def validar_cpf(cpf_cliente):
    """
    Valida o CPF do cliente e verifica se já existe no arquivo.
    """
    cpf_cliente = re.sub(r"[^0-9X]", "", cpf_cliente)

    if len(cpf_cliente) != 11:
        raise TamanhoCPF("Tamanho do CPF excede os limites")

    with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
        for linha in arquivo:
            if cpf_cliente in linha:
                raise CPFJaCadastrado("CPF Inserido já cadastrado")
    return cpf_cliente


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
    if len(outras_infos) != 30 or " " in outras_infos:
        raise FormatoInfo("Informações adicionais não pode conter espaços ou mais do que 30 caracteres")

    return True


def proximo_id():
    """
    Obtém o próximo ID de cliente disponível.
    """
    with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        if len(linhas) <= 1:
            return "0000000001"

        ultimo_id = linhas[-1].split()[0]
        ultimo_id_digitos = "".join(filter(str.isdigit, ultimo_id))
        proximo = int(ultimo_id_digitos) + 1
        return str(proximo).zfill(10)


cadastro_cliente_txt