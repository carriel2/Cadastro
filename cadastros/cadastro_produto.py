import os.path
import re


def proximo_sequencial(nome_arquivo):
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


def adicionar_informacoes_arquivo(
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
        informacoes = f"{id_armazenado}{descricao_armazenada.ljust(50)}{estoque_armazenado.ljust(10)}{preco_armazenado}"
        arquivo.write(f"{informacoes}\n")


def cadastro_produto_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variaveis que devem ser armazenadas
    na ordem correta.
    """
    verificar_arquivo("cadastro_produto.txt")

    id_armazenado = proximo_sequencial("arquivos_cadastro/cadastro_produto.txt")
    descricao_armazenada = desc_produto()
    estoque_armazenado = qtd_estoque()
    preco_armazenado = preco_unitario()

    adicionar_informacoes_arquivo(
        "arquivos_cadastro/cadastro_produto.txt",
        id_armazenado,
        descricao_armazenada,
        estoque_armazenado,
        preco_armazenado,
    )
    print(
        f"ID: {id_armazenado} Descrição Produto: {descricao_armazenada} Estoque: {estoque_armazenado} Preço Unitário: {preco_armazenado}"
    )


def validar_produto(desc_produto):
    """
    Valida a descrição do produto.
    """
    return bool(re.match("^[a-zA-Z0-9]{1,50}$", desc_produto))


def validar_estoque(qtd_estoque):
    """
    Valida a quantidade de produtos disponível em estoque.
    """
    if re.match(r"^[0-9]{1,10}$", qtd_estoque):
        return qtd_estoque
    else:
        print("Quantidade inválida.")
        return None


def validar_preco(preco):
    """
    Valida o preço do produto.
    """
    try:
        preco_float = float(preco.replace(",", "."))
        if preco_float > 0 and len(preco) <= 30:
            return preco
        else:
            if preco_float <= 0:
                print("O preço deve ser maior que zero.")
            else:
                print("Preço inválido.")
            return None
    except ValueError:
        print("Preço inválido.")
        return None


def desc_produto():
    """
    Solicita a descrição do produto ao usuário. POSIÇÃO 11 - 60
    """
    while True:
        descricao_produto = input(
            "Insira a descrição do produto (Máx 50 caracteres e sem espaço): "
        ).upper()
        if validar_produto(descricao_produto):
            return descricao_produto
        else:
            print("Insira uma descrição válida!")


def qtd_estoque():
    """
    Solicita a quantidade de produtos disponíveis em estoque ao usuário. POSIÇÃO 61 - 70
    """
    while True:
        estoque = input(
            "Insira a quantidade de produtos disponíveis em estoque (Máx 10 caracteres): "
        )
        estoque_validado = validar_estoque(estoque)
        if estoque_validado is not None:
            return estoque_validado


def preco_unitario():
    """
    Solicita o preço unitário do produto ao usuário. POSIÇÃO 71 - 80
    """
    while True:
        preco = input(
            "Insira o preço unitário do produto (Máx 10 caracteres): "
        ).strip()
        preco_validado = validar_preco(preco)
        if preco_validado is not None:
            return preco_validado


cadastro_produto_txt
