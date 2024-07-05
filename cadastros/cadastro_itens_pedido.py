from dtos import dtos
from db_connection import get_connection

@staticmethod
def adiciona_itens_pedido(id_pedido, produtos: list[dtos.PedidoDoProdutoDTO], cursor, conn):
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

    return "TESTANDO"