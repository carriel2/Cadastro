from app.validation.estoque import EstoqueValidacao
from app.database.db_connection import get_connection
from app.exceptions.estoque import ProdutoException
from app.dtos import EstoqueDTO


class EstoqueService:

    @staticmethod
    def cadastrar_estoque(body: EstoqueDTO):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            nome_produto = body.nome_produto
            estoque = body.estoque
            preco = body.preco

            EstoqueValidacao.validar_estoque(estoque)
            EstoqueValidacao.validar_preco(preco)
            EstoqueValidacao.validar_nome_produto(nome_produto)

            cursor.execute("""
                INSERT INTO estoque(nome_produto, qtd_estoque, preco_unitario)
                VALUES (%s, %s, %s)
            """, (nome_produto, estoque, preco))

            conn.commit()
            return "Sucesso"

        except ProdutoException as e:
            conn.rollback()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def consultar_estoque():
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM estoque ORDER BY id ASC")
            estoque = cursor.fetchall()

            if not estoque:
                raise ProdutoException("Nenhum cadastro de produtos encontrado em nosso estoque")

            estoque_formatado = [
                {
                    "id": produto[0],
                    "nome_produto": produto[1],
                    "qtd_estoque": produto[2],
                    "preco_unitario": produto[3],
                }
                for produto in estoque
            ]

            return estoque_formatado

        except ProdutoException as e:
            raise e
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def consultar_estoque_id(id: str):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM estoque WHERE id = %s", (id,))
            produto_encontrado = cursor.fetchone()

            if not produto_encontrado:
                raise ProdutoException("Nenhum produto com o ID fornecido encontrado na base de dados.")

            produto_formatado = {
                "id": produto_encontrado[0],
                "nome_produto": produto_encontrado[1],
                "qtd_estoque": produto_encontrado[2],
                "preco_unitario": produto_encontrado[3]
            }

            return produto_formatado

        except ProdutoException as e:
            raise e
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualiza_estoque(id: int, body: EstoqueDTO):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            EstoqueValidacao.validar_nome_produto(body.nome_produto)
            EstoqueValidacao.validar_estoque(body.estoque)
            EstoqueValidacao.validar_preco(body.preco)

            cursor.execute("""
                UPDATE estoque
                SET nome_produto=%s, qtd_estoque=%s, preco_unitario=%s
                WHERE id = %s
            """, (body.nome_produto, body.estoque, body.preco, id))

            conn.commit()
            return "Sucesso"

        except ProdutoException as e:
            conn.rollback()
            raise e
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deleta_produto_estoque(id: int):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM estoque WHERE id = %s", (id,))
            conn.commit()
            return "Sucesso"

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
