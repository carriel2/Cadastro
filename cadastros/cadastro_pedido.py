import os.path
import re
import datetime

from exceptions.exceptions import ClienteNaoEncontrado, DataFuturaError, DataInvalida


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
                arquivo.write("CADASTRO PEDIDO\n0000000001\n")
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
    nome_arquivo, id_pedido, cliente_id, pedido_data, status
):
    """
    Adiciona as informações no arquivo TXT.
    STATUS - POSIÇÃO 41 - 50
    """

    status = "SEPARACAO"
    with open(nome_arquivo, "a") as arquivo:
        pedido_data_sem_barras = pedido_data.replace("/", "")
        id_pedido_formatado = id_pedido.zfill(10)
        cliente_id_formatado = cliente_id.zfill(10)
        pedido_data_formatada = pedido_data_sem_barras
        informacoes = f"{id_pedido_formatado}{cliente_id_formatado}{pedido_data_formatada}{status}"
        arquivo.write(f"{informacoes}\n")


def cadastro_pedido_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variáveis que devem ser armazenadas
    na ordem correta.
    """
    verificar_arquivo("cadastro_pedido.txt")

    cliente_id = id_cliente()
    pedido_data = data_pedido()
    status = "SEPARACAO"

    id_pedido = proximo_sequencial("arquivos_cadastro/cadastro_pedido.txt")
    if id_pedido is not None:
        adicionar_informacoes_arquivo(
            "arquivos_cadastro/cadastro_pedido.txt",
            id_pedido,
            cliente_id,
            pedido_data,
            status,
        )
        print(
            f"ID Pedido: {id_pedido} ID Cliente: {cliente_id} Data do Pedido: {pedido_data} Status: {status}"
        )
    else:
        print(
            "Falha ao gerar o ID do pedido. Por favor, verifique o arquivo e tente novamente."
        )


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


def validar_data_pedido(data_pedido):
    """
    Confere se a data do pedido é uma data válida (dd/mm/aaaa).
    """
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", data_pedido):
        raise DataInvalida("Este formato de data não é válido")

    dia, mes, ano = map(int, data_pedido.split("/"))

    if not (
        1 <= dia <= 31
        and 1 <= mes <= 12
        and ano >= datetime.datetime.now().year
        and mes >= datetime.datetime.now().month
    ):
        raise DataInvalida("Data Inexistente")

    hoje = datetime.datetime.now().date()
    data_formatada = datetime.datetime(ano, mes, dia).date()
    tres_dias_frente = hoje + datetime.timedelta(days=3)
    if hoje <= data_formatada <= tres_dias_frente:
        return True
    else:
        raise DataFuturaError("Data Ultrapassa o limite de 3 dias")


def id_cliente(id):
    """
    Realiza a confirmação se o id do cliente já está cadastrado ou não no TXT. POSIÇÃO 11 - 20
    """
    if not id:
        id_cliente = input("Insira o ID do cliente registrado (10 caracteres): ").zfill(10)

    else:
        id_cliente = id.zfill(10)
    if validar_cliente_id(id_cliente):
        print("Cliente confirmado!")
        return id_cliente
    else:
        raise ClienteNaoEncontrado("Cliente não encontrado, certifique-se de cadastrá-lo!")
        

def data_pedido():
    """
    Realiza o cadastro da data do pedido baseado no DateTime. - POSIÇÃO 21 - 30
    """
    while True:
        data_pedido = input(
            "Insira a data de cadastro do pedido (dd/mm/aaaa) e no máximo 3 dias à frente): "
        )

        if validar_data_pedido(data_pedido):
            print("Cadastro da data realizado!")
            return data_pedido
        else:
            print("Data inválida, certifique-se dela atender a todas as condições!")


cadastro_pedido_txt
