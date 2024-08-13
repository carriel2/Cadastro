from app.validation.pedido import PedidoValidacao
from app.database.db_connection import get_connection
from app.exceptions.estoque import ProdutoException
from app.exceptions.pedido import PedidoException
from app.exceptions.cliente import ClienteException
from app.dtos import PedidoDTO, AdicionarItemDTO, AtualizarItemDTO, DeletaItemDTO


class PedidoService:

    @staticmethod
    def cadastrar_pedido(body: PedidoDTO):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            id_cliente = body.id_cliente
            status_pedido = body.status
            data = body.data
            produtos = body.produtos
            valor_total_pedido = 0

            PedidoValidacao.validar_cliente(id_cliente, cursor)
            PedidoValidacao.validar_data_pedido(data)

            produtos_agrupados = PedidoValidacao.agrupa_produtos(produtos)

            for produto_id, quantidade_pedido in produtos_agrupados.items():
                infos_retorno = PedidoValidacao.validar_produto_e_estoque(produto_id, quantidade_pedido, cursor)

                novoestoque = PedidoValidacao.calcular_novo_estoque(infos_retorno["qtde_estoque"], quantidade_pedido)
                total_parcial = PedidoValidacao.calcular_total_pedido(quantidade_pedido,
                                                                      infos_retorno["preco_unitario"])

                valor_total_pedido += total_parcial

                cursor.execute("""
                    UPDATE public.estoque
                    SET qtd_estoque=%s
                    WHERE id = %s;
                """, (novoestoque, produto_id))

            cursor.execute("""
                INSERT INTO Pedido (id_cliente, data_pedido, valor_total, status, total_itens)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (id_cliente, data, valor_total_pedido, status_pedido, len(produtos_agrupados)))

            id_gerado = cursor.fetchone()[0]

            for produto_id, quantidade_pedido in produtos_agrupados.items():
                cursor.execute("""
                    INSERT INTO itens_pedido (id_produto, id_pedido, qtd_comprada)
                    VALUES (%s, %s, %s)
                """, (produto_id, id_gerado, quantidade_pedido))

            conn.commit()
            return "Sucesso"

        except ClienteException as e:
            conn.rollback()
            raise e
        except (ProdutoException, PedidoException) as e:
            conn.rollback()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def consulta_pedidos():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM pedido
                ORDER BY id ASC
            """)
            pedidos = cursor.fetchall()

            if not pedidos:
                raise PedidoException("Nenhum pedido encontrado na base de dados")

            pedido_formatado = PedidoValidacao.formatar_pedidos(pedidos)
            return pedido_formatado

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def consulta_pedido_id(id_pedido: int):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM VW_PEDIDO_DETALHADO WHERE ID_PEDIDO = %s;
            """, (id_pedido,))
            pedidos = cursor.fetchall()

            if not pedidos:
                raise PedidoException("Pedido não encontrado")

            pedido_formatado = PedidoValidacao.formatar_pedido_detalhado(pedidos)
            return pedido_formatado

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir_item_pedido(id_pedido: int, body: AdicionarItemDTO):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            id_produto = body.id_produto
            quantidade_comprada = body.quantidade_comprada

            PedidoValidacao.validar_pedido_existente(id_pedido, cursor)
            id_e_estoque_valido = PedidoValidacao.validar_produto_e_estoque(id_produto, quantidade_comprada, cursor)

            novo_estoque = PedidoValidacao.calcular_novo_estoque(id_e_estoque_valido["qtde_estoque"],
                                                                 quantidade_comprada)
            total_parcial_pedido = PedidoValidacao.calcular_total_pedido(quantidade_comprada,
                                                                         id_e_estoque_valido["preco_unitario"])

            cursor.execute("""
                UPDATE estoque
                SET qtd_estoque =%s
                WHERE id = %s
            """, (novo_estoque, id_produto))

            cursor.execute("""
                UPDATE pedido
                SET valor_total=%s, total_itens = total_itens + 1
                WHERE id = %s
            """, (total_parcial_pedido, id_pedido))

            cursor.execute("""
                INSERT INTO itens_pedido(id_produto, id_pedido, qtd_comprada)
                VALUES(%s, %s, %s)
            """, (id_produto, id_pedido, quantidade_comprada))

            conn.commit()
            return "Sucesso"

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_item_pedido(body: AtualizarItemDTO):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            id_pedido = body.id_pedido
            id_produto = body.id_produto
            nova_quantidade_comprada = body.quantidade_comprada

            PedidoValidacao.validar_produto_existente(id_produto, cursor)
            PedidoValidacao.validar_item_pedido_existente(id_produto, id_pedido, cursor)

            PedidoValidacao.atualizar_item_pedido(id_pedido, id_produto, nova_quantidade_comprada, cursor)

            conn.commit()
            return "Sucesso"

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deleta_item_pedido(body: DeletaItemDTO):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            id_pedido = body.id_pedido
            id_produto = body.id_produto

            PedidoValidacao.validar_item_pedido_existente(id_produto, id_pedido, cursor)

            cursor.execute("""
                DELETE FROM itens_pedido
                WHERE id_pedido = %s AND id_produto = %s
            """, (id_pedido, id_produto))

            cursor.execute("""
                UPDATE pedido
                SET total_itens = total_itens - 1
                WHERE id = %s
            """, (id_pedido,))

            conn.commit()
            return "Sucesso"

        finally:
            cursor.close()
            conn.close()
