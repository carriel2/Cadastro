from app.exceptions.pedido import PedidoNaoEncontrado, PedidoException
from app.exceptions.cliente import ClienteException
from app.exceptions.estoque import ProdutoException


class PedidoValidacao:

    @staticmethod
    def validar_cliente(id_cliente, cursor):
        cursor.execute("SELECT * FROM clientes WHERE id=%s", (id_cliente,))
        if not cursor.fetchone():
            raise ClienteException("Cliente não encontrado")

    @staticmethod
    def validar_data_pedido(data_pedido):
        if not data_pedido:
            raise PedidoException("Data do pedido inválida")

    @staticmethod
    def agrupa_produtos(produtos):
        produtos_agrupados = {}
        for produto in produtos:
            produto_id = produto.id_produto
            quantidade = produto.quantidade_comprada
            if produto_id in produtos_agrupados:
                produtos_agrupados[produto_id] += quantidade
            else:
                produtos_agrupados[produto_id] = quantidade
        return produtos_agrupados

    @staticmethod
    def validar_produto_e_estoque(produto_id, quantidade_pedido, cursor):
        cursor.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            raise ProdutoException("Produto não encontrado")

        estoque = produto['qtde_estoque']

        if estoque < quantidade_pedido:
            raise ProdutoException("Estoque insuficiente")

        return {
            "qtde_estoque": estoque,
            "preco_unitario": produto['preco_unitario']
        }

    @staticmethod
    def calcular_novo_estoque(estoque_atual, quantidade_pedido):
        return estoque_atual - quantidade_pedido

    @staticmethod
    def calcular_total_pedido(quantidade_pedido, preco_unitario):
        return quantidade_pedido * preco_unitario

    @staticmethod
    def formatar_pedidos(pedidos):
        return [{"id": pedido[0], "data": pedido[1], "valor_total": pedido[2], "status": pedido[3]} for pedido in
                pedidos]

    @staticmethod
    def formatar_pedido_detalhado(pedidos):
        return [{"id_pedido": pedido[0], "id_produto": pedido[1], "quantidade_comprada": pedido[2],
                 "valor_total": pedido[3]} for pedido in pedidos]

    @staticmethod
    def validar_produto_existente(id_produto, cursor):
        cursor.execute("SELECT * FROM produtos WHERE id=%s", (id_produto,))
        if not cursor.fetchone():
            raise ProdutoException("Produto não encontrado")

    @staticmethod
    def validar_item_pedido_existente(id_produto, id_pedido, cursor):
        cursor.execute("SELECT * FROM itens_pedido WHERE id_produto=%s AND id_pedido=%s", (id_produto, id_pedido))
        if not cursor.fetchone():
            raise ProdutoException("Item do pedido não encontrado")

    @staticmethod
    def atualizar_item_pedido(id_pedido, id_produto, nova_quantidade_comprada, cursor):
        cursor.execute("""
            UPDATE itens_pedido
            SET qtd_comprada = %s
            WHERE id_pedido = %s AND id_produto = %s
        """, (nova_quantidade_comprada, id_pedido, id_produto))
