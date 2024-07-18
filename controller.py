from datetime import datetime
import re
from fastapi import FastAPI, status, HTTPException, Request
from db_connection import get_connection

import dtos.dtos as dtos

from exceptions.exceptions import (
    ProdutoNaoEncontrado,
    EstoqueInsuficiente,
    DataInvalida,
    DataFuturaError,
    NomeInvalido,
    TamanhoCPF,
    CaracterInvalidoCPF,
    CPFException,
    FormatoInfo,
    DataNInvalida,
    AnoDataInvalida,
    MesInvalido,
    DiaInvalido, EstoqueInvalido, PrecoZeroError, PrecoError
)


class Validacoes:

    @staticmethod
    def id_pedido(id_pedido, cursor):
        """
        Busca na tabela de pedidos se o id inserido durante o update existe.

        Parâmetros:
            - id_pedido: ID do pedido que será utilizado na função
            - cursor: Parâmetro passado para não haver necessidade de reabrir o cursor

        Retrna:
            - Se o ID foi encontrado no SELECT na tabela de pedidos
        """

        cursor.execute("SELECT * FROM pedido where id = %s", (id_pedido,))
        pedido_existe = cursor.fetchone()

        if not pedido_existe:
            return False
        else:
            return True

    @staticmethod
    def id_cliente(id_cli, cursor):
        """
        Busca na tabela de clientes se o id inserido durante o cadastro de pedido existe.

        Parâmetros:
            - id_cliente: ID do cliente inserido pelo usuário para buscar na tabela de cliente se existe

        Retorna:
            - Se o ID foi encontrado no SELECT na tabela de cliente
        """

        cursor.execute(" SELECT id FROM cliente WHERE id = %s", (id_cli,))
        cliente_existe = cursor.fetchone()

        if not cliente_existe:
            return False
        else:
            return True

    @staticmethod
    def id_produto_e_estoque(produto: dtos.PedidoDoProdutoDTO, cursor):
        """
        Confere se o produto está cadastrado

        """
        cursor.execute("SELECT * FROM estoque WHERE id = %s", (produto.produto_id,))

        produto_encontrado = cursor.fetchone()

        nome_produto_bd = produto_encontrado[1]
        quantidade_estoque_bd = produto_encontrado[2]
        preco_unitario = produto_encontrado[3]

        if not produto_encontrado:
            raise ProdutoNaoEncontrado(
                "O id do produto fornecido não foi encontrado na base de dados."
            )

        if produto.quantidade_pedido > int(quantidade_estoque_bd):
            raise EstoqueInsuficiente(
                f"A quantidade de {nome_produto_bd} no seu pedido é superior ao estoque"
            )

        infos_pedido = {
            "nome_produto": nome_produto_bd,
            "qtde_estoque": quantidade_estoque_bd,
            "qtde_compra": produto.quantidade_pedido,
            "preco_unitario": preco_unitario,
        }
        return infos_pedido

    @staticmethod
    def data_pedido(data_pedido: object) -> object:
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

    @staticmethod
    def nome(nome_cliente: str) -> bool:
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

    @staticmethod
    def cpf(cpf_cliente, cursor):
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

    @staticmethod
    def info(outras_infos):
        """
        Valida as informações adicionais do cliente.
        """
        if len(outras_infos) > 30:
            raise FormatoInfo(
                "Informações adicionais não pode conter mais do que 30 caracteres"
            )

        return True

    @staticmethod
    def nascimento(data_nasc):
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

    @staticmethod
    def estoque(id_produto, quantidade_comprada):

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            SELECT qtd_estoque FROM estoque
            WHERE id = %s
            """, (id_produto,))

            estoque_produto_encontrado = cursor.fetchone()

            if estoque_produto_encontrado <= quantidade_comprada:
                return "Sucesso"
            else:
                raise EstoqueInsuficiente(
                    "O estoqoe do produto informado é inferior a quantidade comprada"
                )

        except EstoqueInsuficiente as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def cadastro_estoque(qtd_estoque):
        """
        Valida a quantidade de produtos disponível em estoque.
        """

        if qtd_estoque < '0':
            raise EstoqueInvalido("Estoque não pode ser inferior a 0")

        if re.match(r"^[0-9]{1,10}$", qtd_estoque):
            return True
        else:
            raise EstoqueInvalido("Quantidade inserida do estoque é inválida")

    @staticmethod
    def cadastro_preco(preco):
        """
        Valida o preço do produto.
        """
        try:
            if preco > 0:
                return preco
            else:
                if preco <= 1:
                    raise PrecoZeroError("O valor deve ser maior do que 0")
                else:
                    raise PrecoError("O preco inserido não é válido")
        except ValueError:
            raise PrecoError("Preço Inválido")

    @staticmethod
    def nome_produto(nome_produto):
        """
        Valida a descrição do produto.
        Permite apenas texto com no máximo 40 caracteres e sem espaços.
        """
        if len(nome_produto) <= 40 and re.match("^[a-zA-Z0-9]+$", nome_produto):
            return True
        else:
            raise NomeInvalido("Insira um  que contenha no maximo 40 caracteres e sem espaços")


@staticmethod
def update_pedido(id_pedido, id_produto, valor_total, cursor, ):
    """
    Função genérica para dar UPDATE na tabela de pedido nos campos de valor_total e total_itens

    Parâmetros:
        - id_pedido = ID do pedido a ser alterado
        - valor_total = Novo valor total do pedido
        - total_itens = Novo total de itens do pedido
        - cursor = Utilizado para manter o cursor open

    Retorna:
        - Se o UPDATE foi um sucesso ou não
    """

    cursor.execute("""
        SELECT total_itens, valor_total FROM pedido
        WHERE id =%s
    """, (id_pedido,))

    infos_parciais = cursor.fetchone()

    cursor.execute("""
        SELECT * from itens_pedido 
        WHERE id_produto =  %s AND id_pedido = %s
    """, (id_produto, id_pedido,))

    item_existe = cursor.fetchone()

    if item_existe[0] != int(id_produto):
        total_itens = infos_parciais[0] + 1

        cursor.execute("""
            UPDATE pedido SET valor_total = %s, total_itens = %s
            WHERE id=%s    
        """, (valor_total, total_itens, id_pedido))

        return "Suceso"

    total_itens = infos_parciais[0]
    valor_total_parcial = infos_parciais[1]

    valor_total_definitivo = valor_total_parcial + valor_total

    cursor.execute("""
        UPDATE pedido SET valor_total=%s, total_itens=%s
         WHERE id=%s
    """, (valor_total_definitivo, total_itens, id_pedido))


@staticmethod
def calcular_total_pedido(qtd_compra, preco_unitario):
    """
    Calcula o total do pedido realizado

    Parâmetros:
        - id_produto: ID do produto utilizado no calculo
        - qtd_compra: Quantidade coletada para saber quantos produtos existem na compra

    Retorna:
        - Um dicionário contendo as informações atualizadas do pedido
    """

    total_compra = qtd_compra * preco_unitario

    return total_compra


@staticmethod
def adiciona_itens_pedido(id_pedido, produtos: list[dtos.PedidoDoProdutoDTO], cursor):
    """
    Insere na tabela de itens_pedido as informações para vincular item-pedido

    Parâmetros:
        - infos: Informações do item de determinado pedido

    Retorna:
        - Uma função que insere as informações no banco
    """

    for produto in produtos:
        print(f"Inserindo id_produto: {produto.produto_id}")
        cursor.execute("""
            INSERT INTO itens_pedido(id_produto, id_pedido, qtd_comprada)
            VALUES(%s, %s, %s)
        """, (produto.produto_id, id_pedido, produto.quantidade_pedido))


@staticmethod
def calcular_novo_estoque(qtd_estoque, qtd_compra):
    """
    Calcula a nova quantidade disponível em estoque de determinado produto

    Parâmetros:
        - qtd_estoque: Quantidade total disponível em estoque de determinado produto
        - qtd_compra: Quantidade total comprada de determinado produto

    Retorna:
        - A nova quantidade disponível em estoque do produto, após realizar a subtração
        qtd_estoque - qtd_compra
    """

    novo_estoque = qtd_estoque - qtd_compra

    return novo_estoque


def calcula_total_pedido(cursor, id_pedido):
    cursor.execute("""
        SELECT SUM(ip.qtd_comprada * e.preco_unitario)
        FROM itens_pedido ip
        JOIN estoque e ON ip.id_produto = e.id
        WHERE ip.id_pedido = %s
    """, (id_pedido,))
    total = cursor.fetchone()[0]
    return total

    """
    Atualiza um item já existente, em um pedido também já existente.

    Parâmetros:
        - Deve receber todas as informações para atualizar um item no pedido:
            - ID do Pedido (Informado via Body)
            - ID do Produto (Informado via Body)
            - Nova quantidade comprada do Produto (Informado via Body)

    Execução:
        - Deve atualizar a tabela de pedido:
            - Valor total deve ser atualizado de acordo com nova quantidade de itens comprados informado no body

        - Deve atualizar a tabela de estoque:
            - Nova quantidade disponível em estoque de acordo com a quantidade comprada informada no body

        - Deve atualizar na tabela itens_pedido
            - Nova quantidade do determinado item comprada.

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar uma mensagem de sucesso.

    Exceções:
        - Exception: Exceção genérica somente para acompanhamento
    """
