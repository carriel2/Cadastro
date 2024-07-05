import os.path
import re

from exceptions.exceptions import DescricaoInvalida, EstoqueInvalido, PrecoError, PrecoZeroError


def proximo_sequencial_2(nome_arquivo):
    """
    Gera o próximo número sequencial e o retorna.
    Se o arquivo não existir, cria o arquivo e escreve o primeiro sequencial.
    """

    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "r") as arquivo:
                linhas = arquivo.readlines()
                if len(linhas) <= 1:
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
                arquivo.write("CADASTRO PRODUTO\n0000000001\n")
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
            arquivo.write("CADASTRO PRODUTO\n")


def adicionar_informacoes_arquivo_3(
        nome_arquivo,
        id_armazenado,
        descricao_armazenada,
        estoque_armazenado,
        preco_armazenado,
):
    """
    Adiciona as informações no arquivo TXT.
    """
    with open(nome_arquivo, "a") as arquivo:
        informacoes = f"{id_armazenado}{descricao_armazenada.ljust(50)}{estoque_armazenado.ljust(10)}{preco_armazenado.ljust(10)}"
        arquivo.write(f"{informacoes}\n")


def cadastro_produto_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variaveis que devem ser armazenadas
    na ordem correta.
    """
    verificar_arquivo("cadastro_produto.txt")

    id_armazenado = proximo_sequencial_2("arquivos_cadastro/cadastro_produto.txt")
    descricao_armazenada = validar_produto()
    estoque_armazenado = validar_estoque()
    preco_armazenado = validar_preco()

    adicionar_informacoes_arquivo_3(
        "arquivos_cadastro/cadastro_produto.txt",
        id_armazenado,
        descricao_armazenada,
        estoque_armazenado,
        preco_armazenado,
    )


def validar_produto(desc_produto):
    """
    Valida a descrição do produto.
    Permite apenas texto com no máximo 40 caracteres e sem espaços.
    """
    if len(desc_produto) <= 40 and re.match("^[a-zA-Z0-9]+$", desc_produto):
        return True
    else:
        raise DescricaoInvalida("Insira uma descrição que contenha no maximo 40 caracteres e sem espaços")


def validar_estoque(qtd_estoque):
    """
    Valida a quantidade de produtos disponível em estoque.
    """

    if qtd_estoque < '0':
        raise EstoqueInvalido("Estoque não pode ser inferior a 0")

    if re.match(r"^[0-9]{1,10}$", qtd_estoque):
        return True
    else:
        raise EstoqueInvalido("Quantidade inserida do estoque é inválida")


def validar_preco(preco):
    """
    Valida o preço do produto.
    """
    try:
        if preco > 0 and len(preco) <= 30:
            return preco
        else:
            if preco <= 1:
                raise PrecoZeroError("O valor deve ser maior do que 0")
            else:
                raise PrecoError("O preco inserido não é válido")
    except ValueError:
        raise PrecoError("Preço Inválido")
