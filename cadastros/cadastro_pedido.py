import os.path
import re
import datetime

from db_connection import get_connection
from dtos.dtos import PedidoDoProdutoDTO
from exceptions.exceptions import (
    ClienteNaoEncontrado,
    DataFuturaError,
    DataInvalida,
    EstoqueInsuficiente,
    ProdutoNaoEncontrado,
)


def proximo_sequencial(nome_arquivo):
    """
    Gera o próximo número sequencial e o retorna.
    Se o arquivo não existir, cria o arquivo e escreve o primeiro sequencial.
    """

    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "r") as arquivo:
                linhas = arquivo.readlines()
                if len(linhas) == 0:
                    proximo = 1
                else:
                    ultimo_sequencial = int(linhas[-1][:10].strip())
                    proximo = ultimo_sequencial + 1

            return str(proximo).zfill(10)

        except Exception as e:
            print("Erro ao ler/escrever no arquivo:", e)
            return None
    else:
        try:
            with open(nome_arquivo, "w") as arquivo:
                arquivo.write("0000000001\n")
            return "0000000001"

        except Exception as e:
            print("Erro ao criar o arquivo:", e)
            return None


def verificar_arquivo(nome_arquivo):
    """
    Verifica se o arquivo existe e cria o cabeçalho se necessário.
    """
    diretorio = "arquivos_cadastro"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    if not os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, "w") as arquivo:
            arquivo.write("CADASTRO PEDIDO\n")


def adicionar_informacoes_arquivo(
        nome_arquivo, id_pedido, cliente_id, pedido_data, status, total_pedido
):
    """
    Adiciona as informações no arquivo TXT.
    STATUS - POSIÇÃO 41 - 50
    """

    with open(nome_arquivo, "a") as arquivo:
        status_pedido = status
        pedido_data_sem_barras = pedido_data.replace("/", "")
        id_pedido_formatado = id_pedido.zfill(10)
        cliente_id_formatado = cliente_id.zfill(10)
        pedido_data_formatada = pedido_data_sem_barras
        informacoes = f"{id_pedido_formatado}{cliente_id_formatado}{pedido_data_formatada}{status_pedido}{total_pedido}"
        arquivo.write(f"{informacoes}\n")


def validar_cliente_id(id_cliente):
    """
    Confere se o cliente está cadastrado
    """
    with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
        for linha in arquivo:
            cliente_id = linha[:10].strip()

            if cliente_id == id_cliente:
                return True

    return False



