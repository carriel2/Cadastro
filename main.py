from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from db_connection import get_connection

from controller import (
    calcular_total_pedido,
    calcular_novo_estoque,
    Validacoes, calcula_total_pedido,

)

from exceptions.exceptions import (
    CPFException,
    ClienteException,
    DataException,
    ProdutoException,
    PedidoException,
)
import dtos.dtos as dtos

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        print(f"Error: {error}")
        if error["type"] == "missing":
            nome_campo = error["loc"][1]
            if nome_campo == "nome":
                errors.append({"msg": "Campo 'nome' é obrigatório"})
            elif nome_campo == "cpf":
                errors.append({"msg": "Campo 'CPF' é obrigatório"})
            elif nome_campo == "data_nasc":
                errors.append({"msg": "Campo 'data_nasc' é obrigatório"})
        elif error["loc"] == ("path", "cpf"):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": "O CPF deve ser válido"}
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.post("/cadastrar/cliente")
def create_cliente(body: dtos.ClienteDTO):
    """
    Cadastra um novo cliente no Sistema e banco de dados.

    Parâmetros:
        -Deve receber todas as informações necessárias para cadastrar um novo cliente.
            - Nome do Cliente(nome_cliente) - Informado via Body.
            - CPF do Cliente(cpf_clienet) - Informado via Body.
            - Data de Nascimento do Cliente(data_nasc) - Informado via Body.
            - Informações Adicionais(inf_adc) - Informado via Body.

        Execução:
            - Deve-se validar o nome do cliente.
            - Deve-se validar a formatação do CPF e se o mesmo é válido.
            - Deve-se validar a data de nascimento do cliente.
            - Deve Inserir todas as informações passadas via Body na tabela de cliente.

        Retorna:
            - Caso tudo ocorra corretamente, deve retornar uma mensagem de sucesso.

        Exceções:
            - CPFException: Exceção Pai para qualquer exceção relacionada ao CPF.
            - DataException: Exceção Pai para qualquer exceção relacionada a data de nascimento.
            - ClienteException: Exceção Pai para qualquer exceção relacionada ao cliente.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        nome_cliente = body.nome
        cpf_cliente = body.cpf
        data_nasc = body.data_nasc
        inf_adc = body.inf_adicionais

        Validacoes.nome(nome_cliente)
        Validacoes.cpf(cpf_cliente, cursor)
        Validacoes.nascimento(data_nasc)

        if inf_adc is not None:
            Validacoes.info(inf_adc)

        cursor.execute("""
            INSERT INTO Cliente (nome, cpf, data_nasc, info_adicional)
            VALUES (%s, %s, %s, %s)
       """, (nome_cliente, cpf_cliente, data_nasc, inf_adc))

        conn.commit()
        return "Sucesso"

    except (CPFException, DataException, ClienteException) as e:
        conn.rollback()
        raise (HTTPException
               (status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conn.close()
        cursor.close()


@app.get("/consulta/clientes")
def consulta_clientes():
    """
    Consulta todos os clientes que estiverem cadastrados na base de dados

    Parâmetros:
        - Não possui nenhum, pois se trata de uma consulta gênérica e geral

    Execução:
        - Executa um SELECT na tabela de clientes, retornando todos eles.
        - Formata os dados dos clientes para se ajustar conforme o retorno

    Retorna:
        - As informações (ID, Nome, Data de Nascimento, Informações Adicionais e CPF) todas elas formatadas e organizdas.

    Exceção:
        - ClienteException: Exceção Pai para qualquer exceção relacionada ao cliente.
        - Exception: Exceção genérica somente para acompanhamento.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
                SELECT * FROM Cliente
            """)
        clientes = cursor.fetchall()
        if not clientes:
            raise ClienteException(
                "Nenhum cliente encontrado na base de dados"
            )

        clientes_formatados = [
            {
                'id': cliente[0],
                'nome': cliente[1],
                'data_nasc': cliente[2],
                'info_adicional': cliente[3],
                'cpf': cliente[4],
            }
            for cliente in clientes
        ]

        return clientes_formatados

    except ClienteException as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conn.close()
        cursor.close()


@app.get("/consulta/cliente/{cpf}")
def consulta_cliente_cpf(cpf: str):
    """
    Consulta um cliente específico baseado no CPF inserido na URL

    Parâmetros::
        - Deve receber o CPF do cliente a ser buscado pela URL

    Execução:
        - Excecuta um SELECT com WHERE na tabela de clientes, buscando por CPF.
        - Formata as informações do cliente (ID, Nome, Data de Nascimento, Informações Adicionais e CPF) para retornar na consulta.

    Exceções:
        - ClienteException: Exceção Pai para qualquer exceção relacionada ao cliente.
        - Exception: Exceção genérica somente para acompanhamento.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT * FROM Cliente WHERE cpf = %s", (cpf,))
        cliente_info = cursor.fetchone()

        if not cliente_info:
            raise ClienteException("Cliente não encontrado")

        cliente_formatado = {
            'id': cliente_info[0],
            'nome': cliente_info[1],
            'data_nasc': cliente_info[2],
            'info_adicional': cliente_info[3],
            'cpf': cliente_info[4],
        }

        return cliente_formatado

    except ClienteException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    finally:
        conn.close()
        cursor.close()


@app.delete("/deleta/cliente/{cpf}")
def deleta_cliente(cpf: str):
    """
    Deleta um cliente pelo CPF inserido na url.

    Parâmetros:
        - Deve receber o CPF do cliente via URL, para realizar a identificação e exclusão do mesmo
            - CPF do cliente que deseja deletar.

    Execução:
        - Deve buscar na tabela de cliente pelo cpf informado na URL, e caso encontrado realizar a exclusão dos dados do cliente.

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar uma mensagem de sucesso

    Exceções:
        - CPFException: Caso o CPF inserido do cliente não seja encontrado
        - ClienteException: Exception para qualquer erro relacionado ao cliente
        - Exception: Exceção genérica somente para acompanhamento

    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("DELETE FROM Cliente WHERE cpf = %s", (cpf,))
        if cursor.rowcount == 0:
            raise CPFException(f"CPF {cpf} não encontrado")

        conn.commit()
        return {"details": "Sucesso",
                "CPF": cpf
                }

    except ClienteException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e

    finally:
        cursor.close()
        conn.close()


@app.post("/cadastrar/pedido")
def cadastrar_pedido(body: dtos.PedidoDTO):
    """
    Realiza o cadastro de um novo pedido.

    Parâmetros:
        - Deve receber todas as informações para criação de um novo pedido:
            - ID do Cliente (Informado via Body)
            - Status do pedido (Informado via Body)
            - Produtos (Informado via Body -  Lista contendo ID do Produto a ser comprado e quantidade comprada)

    Execução:
        - Deve validar o ID do cliente.
        - Deve validar a data do pedido.
        - Deve validar todos os produtos um a um
            - Validar ID do produto para saber se o mesmo está cadastrado na tabela de estoque
            - Validar a quantidade comprada, comparando com o estoque para saber se a quantidade é válida,
            - Atualizar a quantidade disponível em estoque para cada produto dentro do loop for.
            - Realizar o cálculo parcial e total do pedido.
            - Inserir as informações do pedido na tabela referente.
                - id_cliente
                - data_pedido
                - valor_total
                - status
                - total_itens
        - Deve inserir os itens do pedido na tabela itens_pedido
            - id_produto
            - id_pedido
            - qtd_comprada

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar uma mensagem de sucesso

    Exceções:
        - ClienteException: Exceção relacionada a quaisquer erros que ocorram com o cliente.
        - DataException: Esceção relacionada a quaisquer erros que ocorram com a data.
        - ProdutoExceptiom: Exceção relacionada a quaisquer erros que ocorram com o produto.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        id_cliente = body.id_cliente
        status_pedido = body.status
        data = body.data
        produtos = body.produtos
        valor_total_pedido = 0

        cliente_existe = Validacoes.id_cliente(id_cli=id_cliente, cursor=cursor)

        Validacoes.data_pedido(data)

        if not cliente_existe:
            raise ClienteException("ID do cliente não encontrado no cadastro")

        produtos_agrupados = {}
        for produto in produtos:
            if produto.produto_id in produtos_agrupados:
                produtos_agrupados[produto.produto_id] += produto.quantidade_pedido
            else:
                produtos_agrupados[produto.produto_id] = produto.quantidade_pedido

        for produto_id, quantidade_pedido in produtos_agrupados.items():
            infos_retorno = Validacoes.id_produto_e_estoque(
                dtos.PedidoDoProdutoDTO(produto_id=produto_id, quantidade_pedido=quantidade_pedido), cursor=cursor)

            estoque = int(infos_retorno["qtde_estoque"])
            preco_unitario = float(infos_retorno["preco_unitario"])

            novoestoque = calcular_novo_estoque(
                qtd_estoque=estoque, qtd_compra=quantidade_pedido
            )

            total_parcial = calcular_total_pedido(
                qtd_compra=quantidade_pedido, preco_unitario=preco_unitario
            )

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
                SELECT qtd_comprada FROM itens_pedido
                WHERE id_produto = %s AND id_pedido = %s
            """, (produto_id, id_gerado))

            item_existente = cursor.fetchone()

            if item_existente:
                nova_qtd_comprada = item_existente[0] + quantidade_pedido
                cursor.execute("""
                    UPDATE itens_pedido 
                    SET qtd_comprada = %s
                    WHERE id_produto = %s AND id_pedido = %s
                """, (nova_qtd_comprada, produto_id, id_gerado))
            else:
                cursor.execute("""
                    INSERT INTO itens_pedido (id_produto, id_pedido, qtd_comprada)
                    VALUES (%s, %s, %s)
                """, (produto_id, id_gerado, quantidade_pedido))

        conn.commit()
        return "Sucesso"

    except ClienteException as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DataException, ProdutoException) as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Algo inesperado aconteceu. {e}",
        ) from e
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        cursor.close()
        conn.close()


@app.get("/consulta/pedido")
def consulta_pedidos():
    """
    Consulta todos os pedidos que estiverem cadastrados na base de dados.

    Parâmetros:
        - Não possui nenhum, pois se trata de uma consulta genérica e geral.

    Execução:
        - Executa um SELECT na tabela de pedidos, retornando todos eles.
        - Formata os dados dos pedidos para se ajustar conforme o retorno.

    Retorna:
        - As informações (ID, ID do cliente, Data do pedido, Valor total, Status do pedido, Total de itens) todas elas formatadas e organizdas.

    Exceção:
        - ClienteException: Exceção Pai para qualquer exceção relacionada ao cliente.
        - Exception: Exceção genérica somente para acompanhamento.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("""
                SELECT * FROM pedido
                ORDER BY id ASC
            """)
        pedidos = cursor.fetchall()

        if not pedidos:
            raise PedidoException(
                "Nenhum pedido encontrado na base de dados"
            )

        pedido_formatado = [
            {
                "id": pedido[0],
                "id_cliente": pedido[1],
                "data_pedido": pedido[2],
                "valor_total": pedido[3],
                "status_pedido": pedido[4],
                "total_itens": pedido[5]

            }
            for pedido in pedidos
        ]

        return pedido_formatado

    except PedidoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()


@app.get("/consulta/pedido/{id_pedido}")
def consulta_pedido_id(id_pedido: int):
    """
    Consulta os pedidos cadastrados pelo id deles informados na URL.

    Parâmetros:
        - id_pedido: ID do pedido informado via URL, utilizado na busca.

    Execução:
        - Executa um SELECT na tabela de pedidos, utilizando o id_pedido como parâmetro para buscar,
        - Formata os dados do pedido ara se ajustar conforme o retorno.

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar as informações do pedido formatado.

    Exceções:
        - PedidoException: Quando o id do pedido não for encontrado, será retornado essa exceção.
        - Exception: Exceção genérica somente para acompanhamento.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM pedido WHERE id = %s", (id_pedido,))
        pedido_encontrado = cursor.fetchone()

        if not pedido_encontrado:
            raise PedidoException("Pedido não encontrado")

        pedido_formatado = {
            'id': pedido_encontrado[0],
            'id_cliente': pedido_encontrado[1],
            'data_pedido': pedido_encontrado[2],
            'valor_total': pedido_encontrado[3],
            'status': pedido_encontrado[4],
            'total_itens': pedido_encontrado[5]
        }

        return pedido_formatado

    except PedidoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        cursor.close()
        conn.close()


@app.post("/inserir/itempedido/{id}")
def inserir_item_pedido(id: int, body: dtos.AdicionarItemDTO):
    """
    Insere 1 item novo em um pedido já cadastrado.

    Parâmetros:
        - Deve receber todas as informações para inserir o novo item no pedido
            - ID do Pedido (Informado via URL)
            - ID do Produto (Informado via Body)
            - Quantidade comprada do produto (Informado via Body)

    Execução:
        - Deve atualizar na tabela de pedido:
            - O valor total do pedido de acordo com o item novo inserido.

        - Deve atualizar na tabela estoque:
            - A nova quantidade disponível do estoque de determinado comprado, baseado na quantidade comprada

        - Deve inserir na tabela de itens_pedido:
            - ID do Produto (Deve ser validado para verificar se existe na tabela de estoque)
            - Quantidade Comprada (Deve ser validado para verificar se o estoque disponível supre a quantidade comprada)

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar uma mensagem de "Sucesso"

    Exceções:
        - PedidoException: Exceçao para quando o Pedido não é encontrado no BD
        - Exception: Exceção genérica somente para acompanhamento.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        id_pedido = id
        id_produto = body.id_produto
        quantidade_comprada = body.quantidade_comprada

        cursor.execute("""
            SELECT total_itens, valor_total from pedido
            WHERE id = %s
        """, (id_pedido,))

        infos_pedido = cursor.fetchone()

        if not infos_pedido:
            raise PedidoException(
                "Pedido não encontrado na base de dados"
            )

        total_itens = infos_pedido[0]
        valor_total_banco = float(infos_pedido[1])

        total_itens_pedido = total_itens + 1

        id_e_estoque_valido = Validacoes.id_produto_e_estoque(
            dtos.PedidoDoProdutoDTO(produto_id=id_produto, quantidade_pedido=quantidade_comprada), cursor=cursor)

        estoque = int(id_e_estoque_valido["qtde_estoque"])
        preco_unitario = float(id_e_estoque_valido["preco_unitario"])

        novo_estoque = calcular_novo_estoque(qtd_estoque=estoque, qtd_compra=quantidade_comprada)

        total_parcial_pedido = calcular_total_pedido(qtd_compra=quantidade_comprada, preco_unitario=preco_unitario)

        total_final_pedido = total_parcial_pedido + valor_total_banco

        cursor.execute("""
            UPDATE estoque
            SET qtd_estoque =%s
            WHERE id = %s
        """, (novo_estoque, id_produto))

        cursor.execute("""
            UPDATE pedido
            SET valor_total=%s, total_itens = %s
            WHERE id = %s
        """, (total_final_pedido, total_itens_pedido, id_pedido))

        cursor.execute("""
            INSERT INTO itens_pedido(
            id_produto, id_pedido, qtd_comprada)
            VALUES(%s, %s, %s)
        """, (id_produto, id_pedido, quantidade_comprada))

        conn.commit()
        return "Sucesso"

    except PedidoException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        cursor.close()
        conn.close()


@app.put("/alterar/item_pedido/")
def atualizar_item_pedido(body: dtos.AtualizarItemDTO):
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

    conn = get_connection()
    cursor = conn.cursor()

    try:

        id_pedido = body.id_pedido
        id_produto = body.id_produto
        nova_quantidade_comprada = body.quantidade_comprada

        cursor.execute("""
            SELECT qtd_estoque FROM estoque
            WHERE id=%s
        """, (id_produto,))

        infos_estoque = cursor.fetchone()

        cursor.execute("""
            SELECT qtd_comprada FROM itens_pedido
            WHERE id_produto = %s and id_pedido = %s
        """, (id_produto, id_pedido))

        item_pedido = cursor.fetchone()

        if not infos_estoque:
            raise ProdutoException(
                "Produto não encontrado na base de dados"
            )

        qtd_estoque = infos_estoque[0]
        qtd_comprada_banco = item_pedido[0]

        diferenca = nova_quantidade_comprada - qtd_comprada_banco

        novo_estoque = qtd_estoque - diferenca

        cursor.execute("""
            UPDATE estoque
            SET qtd_estoque = %s
            WHERE id = %s
        """, (novo_estoque, id_produto,))

        cursor.execute("""
            UPDATE itens_pedido
            SET qtd_comprada = %s
            WHERE id_produto = %s AND id_pedido = %s
        """, (nova_quantidade_comprada, id_produto, id_pedido,))

        valor_total_atualizado = calcula_total_pedido(cursor, id_pedido)

        cursor.execute("""
            UPDATE pedido
            SET valor_total=%s
            WHERE id = %s
            """, (valor_total_atualizado, id_pedido,))

        conn.commit()
        return "Sucesso"

    except ProdutoException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        cursor.close()
        conn.close()


@app.delete("/delete/pedido/{id}")
def delete_pedido(id: int):
    """
    Deleta um pedido pelo ID.

    Parâmetros:
        - id: ID do pedido a ser deletado.

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar uma mensagem de sucesso.

    Exceções:
        - PedidoException: Exceção para quando o pedido não for encontrado na base de dados.
        - Exception: Exceção genérica somente para acompanhamento.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id from pedido where id = %s
            """, (id,))

        encontrado = cursor.fetchone()

        if not encontrado:
            raise PedidoException(
                'Pedido não encontrado'
            )

        cursor.execute("""
           DELETE FROM itens_pedido WHERE id_pedido = %s           
        """, (id,))

        cursor.execute("""
            DELETE FROM pedido WHERE id = %s
            """, (id,))

        conn.commit()
        return "Sucesso"

    except PedidoException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e

    finally:
        cursor.close()
        conn.close()


@app.post("/cadastrar/estoque/")
def cadastrar_estoque(body: dtos.EstoqueDTO):
    """
    Cadastra um novo produto na tabela de estoque.

    Parâmetros:
        - ID do produto (Gerenciado pelo pgadmin)
        - Nome do produto (Informado via body)
        - Estoque (Informado via body)
        - Preço (Informado via body)

    Execução:
        - Deve inserir na tabela de estoque as informações passadas via body do novo produto.

    Retorna:
        - Caso tudo ocorra corretamente deve retornar uma mensagem de sucesso.

    Exceções:
        - ProdutoException: Exceção para qualquer erro que aconteça durante o cadastro do produto.
        - Exception: Exceção genérica somente para acompanhamento.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        nome_produto = body.nome_produto
        estoque = body.estoque
        preco = body.preco

        Validacoes.cadastro_estoque(qtd_estoque=estoque)
        Validacoes.cadastro_preco(preco=preco)
        Validacoes.nome_produto(nome_produto=nome_produto)

        cursor.execute("""
            INSERT INTO estoque(
            nome_produto, qtd_estoque, preco_unitario)
            VALUES (%s, %s, %s)
        """, (nome_produto, estoque, preco,))

        conn.commit()
        return "Sucesso"

    except ProdutoException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()


@app.get("/consulta/estoque/")
def consultar_estoque():
    """
    Consulta todos os produtos cadastrados no estoque.

    Parâmetros:
        - Não possui pois se trata de uma consulta geral de estoque.

    Execução:
        - Realiza um SELECT sem WHERE na tabela de estoque, retornando os produtos cadastrados.

    Retorna:
        - Os produtos cadastrados na tabela estoque formatados.

    Exceções:
        - ProdutoException: Esceção para caso não exista nenhum produto cadastrado no estoque.
        - Exception: Exceção genérica somente para acompanhamento.

    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT * FROM estoque
            ORDER BY id ASC
        """)

        estoque = cursor.fetchall()

        if not estoque:
            raise ProdutoException(
                "Nenhum cadastro de produtos encontrado em nosso estoque"
            )

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()


@app.get("/consulta/estoque/{id}")
def consultar_estoque_id(id: str):
    """
    Consulta um produto específico no cadastro de estoque, de acordo com o ID informado na URL

    Parâmetros:
        - Recebe o ID do produto inserido na URL.

    Execução:
        - Realiza um SELECT com WHERE do id_produto, retornando o produto buscado formatado.

    Retorna:
        - O produto cadastrado na tabela de estoque formatado.

    Exceções:
        - ProdutoException: Exceção para caso o produto não seja encontrado na tabela de estoque.
        - Exception: Exceção genérica somente para acompanhamento.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM estoque WHERE id = %s", (id,))
        produto_encontrado = cursor.fetchone()

        if not produto_encontrado:
            raise ProdutoException(
                "Nenhum produto com o ID fornecido encontrado na base de dados."
            )

        produto_formatado = {
            "id": produto_encontrado[0],
            "nome_produto": produto_encontrado[1],
            "qtd_estoque": produto_encontrado[2],
            "preco_unitario": produto_encontrado[3]
        }

        return produto_formatado

    except ProdutoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()


@app.put("/atualiza/estoque/{id}")
def atualiza_estoque(id: int, body: dtos.EstoqueDTO):
    """
    Atualiza um produto de acordo com o ID fornecido na URL.

    Parâmetros:
        - ID do Produto cadastrado no estoque que vai ser atualizado
        - Informações novas do produto informado via body:
            - nome_produto: Novo nome do produto
            - qtd_estoque: Nova quantidade em estoque do produto
            - preco_unitario: Novo preco unitario do produto.

    Retorna:
        - Caso tudo ocorra corretamente deve retornar uma mensagem de sucesso.

    Exceções:
        - ProdutoException: Caso alguma validação das novas informações falhe.
        - Exception: Exceção genérica somente para acompanhamento.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        Validacoes.nome_produto(body.nome_produto)
        Validacoes.cadastro_estoque(body.estoque)
        Validacoes.cadastro_preco(body.preco)

        cursor.execute("""
        UPDATE estoque
            SET nome_produto=%s, qtd_estoque=%s, preco_unitario=%s
            WHERE id = %s;
            """, (body.nome_produto, body.estoque, body.preco, id,))

        conn.commit()

        return body

    except ProdutoException as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@app.delete("/deleta/produto/{id}")
def deleta_produto_estoque(id: int):
    """
    Deleta um pedido pelo ID informado na URL.

    Parâmetros:
        - ID do produto a ser deletado no estoque.

    Execução:
        - Valida se o id do produto está vinculado a algum pedido.
        - Deleta o produto na tabela de estoque.

    Exceções:
        - ProdutoException: Caso o produto não seja encontrado no estoque ou existam pedidos com esse produto incluso retorna essa exceção.
        - Exception: Exceção genérica somente para acompanhamento.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT * from itens_pedido
            WHERE id_produto = %s
            """, (id,))

        if cursor.rowcount >= 1:
            raise ProdutoException(
                "Existem pedidos com esse produto incluso, por gentileza exclua-os antes de continuar."
            )

        elif cursor.rowcount == 0:
            raise ProdutoException(
                "Produto não encontrado no estoque"
            )

        cursor.execute("""
            DELETE FROM estoque
            where id = %s
        """, (id,))

        conn.commit()
        return "Sucesso"

    except ProdutoException as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()


@app.put("/atualiza/cliente/{id}")
def atualizar_cliente(id: str, body: dtos.AtualizaClienteDTO):
    """
    Atualiza os dados cadastrais de um cliente de acordo com o id fornecido na URL.

    Parâmetros:
        - Recebe o ID do cliente a ser alterado na URL.
        - Recebe informações para atualizar a tabela de cliente via body
            - nome: Novo nome a ser atualizado.
            - data_nasc: Nova data de nascimento a ser atualizada.
            - inf_adicionais: Nova informação adicional a ser atualizada.

    Execução:
        - Recebe todas as informações a serem atualizadas e realiza um UPDATE na tabela de clientes,
        utilizando o ID do cliente no WHERE.

    Retorna:
        - Caso tudo ocorra corretamente, deve retornar uma mensagem de sucesso.

    Exceção:
        - Exception: Exceção genérica somente para acompanhamento.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        nome = body.nome
        data_nasc = body.data_nasc
        inf_adicionais = body.inf_adicionais

        Validacoes.nome(nome_cliente=nome)
        Validacoes.nascimento(data_nasc=data_nasc)
        Validacoes.info(outras_infos=inf_adicionais)

        cursor.execute("""
            UPDATE cliente
            SET nome=%s, data_nasc=%s, info_adicional=%s
            WHERE id=%s
        """, (nome, data_nasc, inf_adicionais, id))

        conn.commit()
        return "Sucesso"

    except (CPFException, DataException, ClienteException) as e:
        conn.rollback()
        raise (HTTPException
               (status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)))

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print('O print do pé do predo é preto?')
    uvicorn.run(app, host="0.0.0.0", port=8000)
