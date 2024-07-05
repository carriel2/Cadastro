from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from db_connection import get_connection
from decouple import config

from cadastros.cadastro_cliente import (
    validar_cpf,
    validar_info,
    validar_nasc,
    validar_nome,
)
from cadastros.cadastro_produto import (
    adicionar_informacoes_arquivo_3,
    proximo_sequencial_2,
    validar_estoque,
    validar_preco, validar_produto,
)
from cadastros.cadastro_pedido import (
    validar_data_pedido,
    verificar_arquivo,
)
from exceptions.exceptions import (
    CPFException,
    ClienteException,
    DataException,
    ProdutoException,
    PedidoException, EstoqueInsuficiente, ProdutoNaoEncontrado,
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
    Cadastra um novo cliente.

    Parâmetros:
        body: Objeto PedidoDTO contendo as informações do cliente.

    Retorna:
        - Objeto ClienteDTO do cliente cadastrado.1

    Lança:
        - HTTPException: Se ocorrer um erro durante o cadastro do cliente.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        nome_cliente = body.nome
        cpf_cliente = body.cpf
        data_nasc = body.data_nasc
        inf_adc = body.inf_adicionais

        validar_nome(nome_cliente)
        validar_cpf(cpf_cliente, cursor)

        if inf_adc is not None:
            validar_info(inf_adc)

        validar_nasc(data_nasc)

        cursor.execute("""
            INSERT INTO Cliente (nome, cpf, data_nasc, info_adicional)
            VALUES (%s, %s, %s, %s)
       """, (nome_cliente, cpf_cliente, data_nasc, inf_adc))

        conn.commit()
        cursor.close()
        conn.close()
        url = f"{config('URL_ENV')}{cpf_cliente}"
        return {"url": url}

    except (CPFException, DataException, ClienteException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/consulta/cliente")
def get_clientes():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Cliente
            """)
            clientes = cursor.fetchall()

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

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/consulta/cliente/{cpf}")
def get_clientes_cpf(cpf: str):
    """
    Consulta um cliente específico baseado no CPF inserido na url

    Retorna:
        - As informações específicas do cliente buscado
    """

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.delete("/delete/cliente/{cpf}")
def delete_cliente(cpf: str):
    """
    Deleta um cliente pelo CPF inserido na url.

    Parâmetros:
        - cpf: CPF do cliente a ser deletado.

    Retorna:
        - Uma mensagem de sucesso.

    Exceções:
        - HTTPException: Se ocorrer um erro durante a deleção do cliente.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Cliente WHERE cpf = %s", (cpf,))
            if cursor.rowcount == 0:
                raise ClienteException(f"CPF {cpf} não encontrado")

            conn.commit()
            return {"details": "Sucesso",
                    "CPF": cpf
                    }

    except ClienteException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e

    finally:
        conn.close()


@app.post("/cadastrar/pedido")
def create_pedido(body: dtos.PedidoDTO):
    """
    Cadastra um novo pedido.

    Parâmetros:
        body: Objeto PedidoDTO contendo as informações do pedido.

    Retorna:
        - Objeto PedidoDTO do pedido cadastrado.

    Exceções:
        - HTTPException: Se ocorrer um erro durante o cadastro do pedido.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        id_cliente = body.id_cliente
        status_pedido = body.status
        data = body.data
        produtos = body.produtos
        valor_total_pedido = 0

        funcoes_auxiliares = FuncoesAuxiliares()
        cliente_existe = funcoes_auxiliares.validar_id_cliente(id_cli=id_cliente, cursor=cursor)

        validar_data_pedido(data)

        if not cliente_existe:
            raise ClienteException("ID do cliente não encontrado no cadastro")

        for produto in produtos:
            infos_retorno = funcoes_auxiliares.validar_id_produto(produto, cursor=cursor)

            estoque = int(infos_retorno["qtde_estoque"])
            produtos_na_compra = int(infos_retorno["qtde_compra"])
            preco_unitario = float(infos_retorno["preco_unitario"])
            nome_produto = infos_retorno["nome_produto"]

            novoestoque = FuncoesAuxiliares.calcular_novo_estoque(
                qtd_estoque=estoque, qtd_compra=produtos_na_compra
            )

            total_parcial = FuncoesAuxiliares.calcular_total_pedido(
                qtd_compra=produtos_na_compra, preco_unitario=preco_unitario
            )

            valor_total_pedido += total_parcial

            cursor.execute("""
               UPDATE public.estoque
               SET qtd_estoque=%s
               WHERE id = %s;
            """, (novoestoque, produto.produto_id))

        cursor.execute("""
            INSERT INTO Pedido (id_cliente, data_pedido, valor_total, status, total_itens)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (id_cliente, data, valor_total_pedido, status_pedido, len(produtos)))

        id_gerado = cursor.fetchone()

        for produto in produtos:
            cursor.execute("""
                SELECT qtd_comprada FROM itens_pedido
                WHERE id_produto = %s AND id_pedido = %s
            """, (produto.produto_id, id_gerado))

            item_existente = cursor.fetchone()

            if item_existente:
                nova_qtd_cpmprada = item_existente[0] + produto.quantidade_pedido
                cursor.execute("""
                    UPDATE itens_pedido 
                    SET qtd_comprada = %s
                    WHERE id_produto = %s AND id_pedido = %s
                """, (nova_qtd_cpmprada, produto.produto_id, id_gerado))

            else:
                cursor.execute("""
                    INSERT INTO itens_pedido (id_produto, id_pedido, qtd_comprada)
                    VALUES (%s, %s, %s)
                
                """, (produto.produto_id, id_gerado, produto.quantidade_pedido))
                FuncoesAuxiliares.adiciona_itens_pedido(id_pedido=id_gerado, produtos=produtos, cursor=cursor)

                conn.commit()
        return body

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
        conn.close()


@app.get("/consulta/pedido")
def get_pedidos():
    """
    Consulta todos os pedidos cadastrados.

    Retorna:
        - Uma lista de pedidos formatados.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM pedido
                ORDER BY id asc
            """)
            pedidos = cursor.fetchall()

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

            cursor.close()
            return pedido_formatado

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/adicionar/itenspedido/")
def adc_itens_pedido(body: dtos.ItensPedidoDTO):
    """
    Adiciona itens a um pedido já existente na tabela itens_pedido

    Parâmetros:
        - body: Informações do item que deseja adicionar ao pedido existente

    Retorna:
        - Informações do item adicionado no pedido.

    Exceções:
        - Exceções genéricas e específicas dentro de cada função chamada
    """

    conn = get_connection()
    cursor = conn.cursor()

    qtd_comprada = body.quantidade_comprada
    id_produto = body.id_produto
    id_pedido = body.id_pedido

    pedido_encontrado = FuncoesAuxiliares.validar_id_pedido(id_pedido=id_pedido, cursor=cursor)

    if not pedido_encontrado:
        raise PedidoException(
            "Pedido não encontrado na base de dados, certifique-se de cadastrá-lo"
        )

    retorno = FuncoesAuxiliares.validar_id_produto(
        produto=dtos.PedidoDoProdutoDTO(produto_id=id_produto, quantidade_pedido=qtd_comprada), cursor=cursor)

    try:
        cursor.execute("""
        SELECT qtd_comprada from itens_pedido
        WHERE id_produto = %s AND id_pedido = %s
        """, (id_produto, id_pedido))

        item_existente = cursor.fetchone()

        if item_existente:

            nova_qtd_comprada = item_existente[0] + qtd_comprada
            cursor.execute("""
                UPDATE itens_pedido 
                SET qtd_comprada = %s 
                WHERE id_produto = %s AND id_pedido = %s
                
            """, (nova_qtd_comprada, id_produto, id_pedido))

        else:
            cursor.execute("""
                INSERT into itens_pedido(id_produto, id_pedido, qtd_comprada) 
                VALUES (%s, %s, %s)
            """, (id_produto, id_pedido, qtd_comprada))

        valor_total = FuncoesAuxiliares.calcular_total_pedido(qtd_compra=qtd_comprada,
                                                              preco_unitario=retorno['preco_unitario'])

        FuncoesAuxiliares.update_pedido(id_pedido=id_pedido, valor_total=valor_total, total_itens=1, cursor=cursor)

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.commit()
        cursor.close()
        conn.close()


# @app.put("/alterar/pedido/{id}")
# def update_pedido(id: str, body: dtos.UpdatePedidoDTO):
#     """
#     Altera pedido baseado no ID informado na URL
#
#     Parâmetros:
#         - id: ID do pedido que deseja realizar a alteração
#         - body: Informações do pedido a serem atualizadas
#
#     Retorna:
#         - Informações do pedido atualizadas, de acordo com as novas passadas
#
#     Exceções:
#         - HTTPException caso ocorra algum erro durante a atualização do pedido
#
#     """
#
#     conn = get_connection()
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute("SELECT * FROM Pedido WHERE id = %s", (id,))
#
#         produto_existente = cursor.fetchone()
#
#         id_pedido = produto_existente[0]
#         id_cliente = produto_existente[1]
#         data_pedido = produto_existente[2]
#         valor_total = produto_existente[3]
#         status_pedido = produto_existente[4]
#         total_itens_pedido = produto_existente[5]
#
#         novo_status_pedido = body.novo_status
#
#         novo_id_cliente = body.id_cliente
#         FuncoesAuxiliares.validar_id_cliente(id_cli=novo_id_cliente, cursor=cursor)
#
#         nova_data_pedido = body.nova_datapedido
#         validar_data_pedido(nova_data_pedido)
#
#         if body.


# except PedidoException as e:
#     conn.rollback()
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
#     )
# except Exception as e:
#     conn.rollback()
#     raise HTTPException(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
#     )
#

@app.delete("/delete/pedido/{id}")
def delete_pedido(id: str):
    """
    Deleta um pedido pelo ID.

    Parâmetros:
        - id: ID do pedido a ser deletado.

    Retorna:
        - Uma mensagem de sucesso.

    Exceções:
        - HTTPException: Se ocorrer um erro durante a deleção do pedido.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:

            encontrado = cursor.execute(
                """
                SELECT * from pedido where id = %s
                """, (id,))

            if not encontrado:
                raise PedidoException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Pedido não encontrado'
                )

            cursor.execute(
                """
                DELETE FROM pedido WHERE id = %s
                """, (id,))

    except PedidoException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            stauts_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=str(e)
        ) from e


@app.post("/cadastrar/produto")
def create_produto(body: dtos.EstoqueDTO):
    """
    Cadastra um novo produto.

    Args:
        body: Objeto EstoqueDTO contendo as informações do produto.

    Retorna:
        - Objeto EstoqueDTO do produto cadastrado.

    Lança:
        - HTTPException: Se ocorrer um erro durante o cadastro do produto.
    """
    try:
        verificar_arquivo("cadastro_produto.txt")

        id_produto = proximo_sequencial_2("arquivos_cadastro/cadastro_produto.txt")
        descricao = body.descricao
        estoque = body.estoque
        preco = body.preco

        validar_produto(descricao)
        validar_estoque(estoque)
        validar_preco(preco)
        adicionar_informacoes_arquivo_3(
            "arquivos_cadastro/cadastro_produto.txt",
            id_produto,
            descricao,
            estoque,
            preco,
        )
        return body

    except ProdutoException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# @app.get("/consulta/produtos")
# def get_produtos():
#     """
#     Consulta todos os produtos cadastrados.
#
#     Retorna:
#         - Uma lista de produtos formatados
#     """
#     diretorio = "arquivos_cadastro"
#     caminho_arquivo = os.path.join(diretorio, "cadastro_produto.txt")
#
#     return Consultas.consultar_arquivo(caminho_arquivo)


@app.get("/consulta/produtos/{id}")
def get_produtos_por_id(id: str):
    """
    Consulta os produtos baseado no ID inserido na URL

    Parâmetros:
        - ID do produto a ser consultado

    Retorna:
        - Informações do produto com o id correspondente

    Exceções:
        - HTTP Exception caso haja algum erro durante as buscas por ID
    """
    id_produto = id.zfill(10)

    try:
        with open("arquivos_cadastro/cadastro_produto.txt", "r") as arquivo:
            for linha in arquivo:
                id_produto_txt = linha[:10]
                nome_produto_txt = linha[10:60].strip()
                estoque_produto_txt = linha[60:70].strip()
                preco_unitario_txt = linha[70:80].strip()

                if id_produto == id_produto_txt:
                    retorno_consulta = {
                        "id_produto": id_produto_txt,
                        "nome_produto": nome_produto_txt,
                        "estoque_produto": estoque_produto_txt,
                        "preco_unitario": preco_unitario_txt,
                    }
                    return retorno_consulta

            raise ProdutoException("Produto não Encontrado")

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de cadastro não encontrado",
        )
    except ProdutoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.put("/alterar/produto/{id}")
def update_produtos(id: int, body: dtos.EstoqueDTO):
    """
    Altera um produto de acordo com o ID fornecido na URL

    Parâmetros:
        - id: ID do produto a ser atualizado
        - body: Informações do produto para serem atualizados

    Retorna:
        - Os dados alterados do produto

    Exceções:
        - HTTP Exception caso ocorra algum erro durante os processos de atualização
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        validar_produto(body.nome_produto)
        validar_estoque(body.estoque)
        validar_preco(body.preco)

        update_banco = cursor.execute("""
        UPDATE public.estoque
            SET nome_produto=%s, qtd_estoque=%s, preco_unitario=%s
            WHERE id = %s;
            """, (body.nome_produto, body.estoque, body.preco, id,))

        conn.commit()

        return body

    except ProdutoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@app.delete("/delete/produto/{id}")
def delete_produto(id: str):
    """
    Deleta um produto pelo ID.

    Parâmetros:
        - id: ID do produto a ser deletado.

    Retorna:
        - Uma mensagem de sucesso.

    Exceções:
        - HTTPException: Se ocorrer um erro durante a deleção do produto.
    """

    id_produto = id.rjust(10, "0")
    try:
        with open("arquivos_cadastro/cadastro_produto.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            encontrado = False
            arquivo.seek(0)
            for linha in linhas:
                if linha.startswith(id_produto):
                    encontrado = True
                    continue
                arquivo.write(linha)
                arquivo.truncate()

            if encontrado:
                return "Sucesso"
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID do produto não encontrado",
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@app.put("/alterar/cliente/{id}")
def update_cliente(id: str, body: dtos.ClienteDTO):
    """
    Atualiza as informações de um cliente.

    Parâmetros:
        - id: ID do cliente a ser atualizado.
        - body: Objeto ClienteDTO contendo as novas informações do cliente.

    Retorna:
        - Objeto ClienteDTO do cliente atualizado.

    Exceções:
        - HTTPException: Se ocorrer um erro durante a atualização do cliente.
    """
    id_cliente = id.zfill(10)

    try:
        encontrado = False
        clientes_atualizados = []
        with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                if linha.startswith(id_cliente):
                    encontrado = True
                    novo_nome = body.nome
                    novo_cpf = body.cpf
                    nova_data_nascimento = body.data_nasc
                    info_adicionais = body.inf_adicionais

                    validar_nome(novo_nome)
                    validar_cpf(novo_cpf)
                    validar_nasc(nova_data_nascimento)
                    validar_info(info_adicionais)

                    nova_data_nascimento = nova_data_nascimento.replace("/", "")

                    linha = (
                            id_cliente.ljust(10)
                            + novo_nome.ljust(40)
                            + novo_cpf.ljust(11)
                            + nova_data_nascimento.ljust(8)
                            + info_adicionais[:30].ljust(30)
                            + "\n"
                    )
                clientes_atualizados.append(linha)

            if not encontrado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado",
                )

            with open("arquivos_cadastro/cadastro_cliente.txt", "w") as arquivo:
                arquivo.writelines(clientes_atualizados)

            return body

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de cadastro não encontrado",
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


class FuncoesAuxiliares:

    @staticmethod
    def update_pedido(id_pedido, valor_total, total_itens, cursor, ):
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
        """, id_pedido)

        infos_parciais = cursor.fetchone()

        total_itens_parcial = infos_parciais[0]
        valor_total_parcial = infos_parciais[1]

        valor_total_definitivo = valor_total_parcial + valor_total
        quantidade_total_definitiva = total_itens_parcial + total_itens

        cursor.execute("""
            UPDATE pedido SET valor_total=%s, total_itens=%s
            WHERE id=%s
        """, (valor_total_definitivo, quantidade_total_definitiva, id_pedido))

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

    @staticmethod
    def validar_id_pedido(id_pedido, cursor):
        """
        Busca na tabela de pedidos se o id inserido durante o update existe.

        Parâmetros:
            - id_pedido: ID do pedido que será utilizado na função
            - cursor: Parâmetro passado para não haver necessidade de reabrir o cursor

        Retrna:
            - Se o ID foi encontrado no SELECT na tabela de pedidos
        """

        cursor.execute("SELECT * FROM pedido where id = %s", (id_pedido))
        pedido_existe = cursor.fetchone()

        if not pedido_existe:
            return False
        else:
            return True

    @staticmethod
    def validar_id_cliente(id_cli, cursor):
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
    def validar_id_produto(produto: dtos.PedidoDoProdutoDTO, cursor):
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


if __name__ == "__main__":
    print('O print do pé do predo é preto?')
    uvicorn.run(app, host="0.0.0.0", port=8000)
