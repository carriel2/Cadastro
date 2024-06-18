from fastapi import FastAPI, HTTPException, status
import uvicorn
from cadastros.cadastro_cliente import (
    adicionar_informacoes_arquivo_2,
    proximo_id,
    validar_cpf,
    validar_info,
    validar_nasc,
    validar_nome,
    verificar_arquivo,
)
from cadastros.cadastro_produto import (
    adicionar_informacoes_arquivo_3,
    proximo_sequencial_2,
    validar_estoque,
    validar_preco,
    validar_produto,
)
from consultas.consultas import Consultas
from cadastros.cadastro_pedido import (
    adicionar_informacoes_arquivo,
    proximo_sequencial,
    validar_data_pedido,
    validar_id_produto,
    verificar_arquivo,
    id_cliente,
)
from exceptions.exceptions import (
    CPFException,
    ClienteException,
    DataException,
    ProdutoException,
    ProdutoNaoEncontrado,
)
import dtos.dtos as dtos
import os

app = FastAPI()


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
    try:
        verificar_arquivo("cadastro_pedido.txt")
        verificar_arquivo("cadastro_itens_pedido.txt")

        id_pedido = proximo_sequencial("arquivos_cadastro/cadastro_pedido.txt")
        cliente_id = id_cliente(body.id_cliente)
        situacao = body.status
        data = body.data
        produtos = body.produtos

        for produto in produtos:
            valor_retorno = validar_id_produto(produto)

            estoque = int(valor_retorno["qtde_estoque"])
            produtos_na_compra = int(valor_retorno["qtde_compra"])

            novoestoque = FuncoesAuxiliares.calcular_novo_estoque(
                qtd_compra=produtos_na_compra, qtd_estoque=estoque
            )

            calcula_total_pedido = FuncoesAuxiliares.calcular_total_pedido(
                id_produto=produto.produto_id, qtd_compra=produtos_na_compra
            )

            total_pedido = str(calcula_total_pedido["total_do_pedido"])
            preco_unitario = str(calcula_total_pedido["preco_unitario_txt"])
            descricao_produto = str(calcula_total_pedido["descricao_produto_txt"])

            produto_atualizado = dtos.ProdutoDTO(
                descricao=str(descricao_produto),
                estoque=str(novoestoque),
                preco=preco_unitario,
            )
            update_produtos(id=produto.produto_id, body=produto_atualizado)

            item = dtos.ItensPedidoDTO(
                id_produto=produto.produto_id,
                id_pedido=id_pedido,
                quantidade_comprada=produtos_na_compra,
                descricao=descricao_produto,
            )
            FuncoesAuxiliares.escreve_itens_pedido(item)

        validar_data_pedido(data)
        adicionar_informacoes_arquivo(
            "arquivos_cadastro/cadastro_pedido.txt",
            id_pedido,
            cliente_id,
            data,
            situacao,
            total_pedido,
        )

        return body

    except ClienteException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DataException, ProdutoException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(f"Algo inesperado aconteceu. {e}"),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/consulta/pedido")
def get_pedidos():
    """
    Consulta todos os pedidos cadastrados.

    Retorna:
        - Uma lista de pedidos formatados.
    """
    diretorio = "arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_pedido.txt")
    formatar_funcao = Consultas.formatar_pedido

    return Consultas.consultar_arquivo(caminho_arquivo, formatar_funcao)


@app.get("/consulta/cliente")
def get_clientes():
    """
    Consulta todos os clientes cadastrados.

    Retorna:
        - Uma lista de clientes formatados.
    """
    diretorio = "arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_cliente.txt")
    formatar_funcao = Consultas.formatar_cliente

    return Consultas.consultar_arquivo(caminho_arquivo, formatar_funcao)


@app.put("/alterar/pedido/{id}")
def update_pedido(id: str, body: dtos.PedidoDTO):
    """
    Altera pedido baseado no ID informado na URL

    Parâmetros:
        - id: ID do pedido que deseja realizar a alteração
        - body: Informações do pedido a serem atualizadas

    Retorna:
        - Informações do pedido atualizadas, de acordo com as novas passadas

    Exceções:
        - HTTPException caso ocorra algum erro durante a atualização do pedido

    """

    id_pedido = id.zfill(10)

    try:
        encontrado = False
        pedido_atualizado = []

        with open("arquivos_cadastro/cadastro_pedido.txt", "r") as arquivo:
            primeira_linha = arquivo.readline()
            for linha in arquivo:
                if linha.startswith(id_pedido):
                    encontrado = True
                    cliente_id = id_cliente(body.id_cliente)
                    novo_status = body.status
                    nova_data = body.data

                    validar_data_pedido(nova_data)
                    nova_data_formatada = nova_data.replace("/", "")

                    linha_atualizada = (
                            str(id_pedido)
                            + str(cliente_id)
                            + nova_data_formatada
                            + novo_status
                            + "\n"
                    )
                    pedido_atualizado.append(linha_atualizada)
                else:
                    pedido_atualizado.append(linha)

        if not encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado"
            )

        with open("arquivos_cadastro/cadastro_pedido.txt", "w") as arquivo:
            arquivo.write(primeira_linha)
            arquivo.writelines(pedido_atualizado)

        return body

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo 'cadastro_pedido.txt' não encontrado.",
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


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
    id_pedido = id.rjust(10, "0")
    try:
        with open("arquivos_cadastro/cadastro_pedido.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            encontrado = False
            arquivo.seek(0)
            for linha in linhas:
                if linha.startswith(id_pedido):
                    encontrado = True
                    continue
                arquivo.write(linha)
                arquivo.truncate()

            if encontrado:
                return "Sucesso"
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido não encontrado",
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            stauts_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=str(e)
        ) from e


@app.post("/cadastrar/produto")
def create_produto(body: dtos.ProdutoDTO):
    """
    Cadastra um novo produto.

    Args:
        body: Objeto ProdutoDTO contendo as informações do produto.

    Retorna:
        - Objeto ProdutoDTO do produto cadastrado.

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


@app.get("/consulta/produtos")
def get_produtos():
    """
    Consulta todos os produtos cadastrados.

    Retorna:
        - Uma lista de produtos formatados
    """
    diretorio = "arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_produto.txt")

    return Consultas.consultar_arquivo(caminho_arquivo)


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
def update_produtos(id: str, body: dtos.ProdutoDTO):
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
    id_produto = id

    try:
        encontrado = False
        produtos_atualizados = []

        with open("arquivos_cadastro/cadastro_produto.txt", "r") as arquivo:
            for linha in arquivo:
                if linha.startswith(id_produto.zfill(10)):
                    encontrado = True
                    nova_desc = body.descricao
                    novo_estoque = str(body.estoque)
                    novo_preco = str(body.preco)

                    validar_produto(nova_desc)
                    validar_estoque(novo_estoque)
                    validar_preco(novo_preco)

                    linha_atualizada = (
                            str(id_produto).zfill(10)
                            + nova_desc.ljust(50)
                            + novo_estoque.ljust(10)
                            + novo_preco.ljust(10)
                            + "\n"
                    )
                    produtos_atualizados.append(linha_atualizada)
                else:
                    produtos_atualizados.append(linha)

        if not encontrado:
            raise ProdutoNaoEncontrado("Produto não encontrado")

        with open("arquivos_cadastro/cadastro_produto.txt", "w") as arquivo:
            arquivo.writelines(produtos_atualizados)

        return body

    except ProdutoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo 'cadastro_produto.txt' não encontrado.",
        )
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


@app.post("/cadastrar/cliente")
def create_cliente(body: dtos.ClienteDTO):
    """
    Cadastra um novo cliente.

    Parâmetros:
        body: Objeto PedidoDTO contendo as informações do cliente.

    Retorna:
        - Objeto ClienteDTO do clienet cadastrado.

    Lança:
        - HTTPException: Se ocorrer um erro durante o cadastro do cliente.
    """

    try:
        print("OIIIII")
        verificar_arquivo("cadastro_cliente.txt")

        cliente_id = proximo_id()
        nome_cliente = body.nome
        cpf_cliente = body.cpf
        data_nasc = body.data_nasc
        inf_adc = body.inf_adicionais

        validar_nome(nome_cliente)
        validar_cpf(cpf_cliente)
        validar_info(inf_adc)
        validar_nasc(data_nasc)

        data_nasc_formatada = data_nasc.replace("/", "")

        adicionar_informacoes_arquivo_2(
            "arquivos_cadastro/cadastro_cliente.txt",
            cliente_id,
            nome_cliente,
            cpf_cliente,
            data_nasc_formatada,
            inf_adc,
        )

        return body

    except (CPFException, DataException, ClienteException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/consulta/cliente")
def get_clientes():
    """
    Consulta todos os clientes cadastrados.

    Retorna:
        - Uma lista de clientes formatados.
    """
    diretorio = "arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_cliente.txt")
    formatar_funcao = Consultas.formatar_cliente

    return Consultas.consultar_arquivo(caminho_arquivo, formatar_funcao)


@app.get("/consulta/cliente/{id}")
def get_clientes_id(id: str):
    """
    Consulta um cliente específico baseado no ID inserido na url
    
    Retorna:
        - As informações específicas do cliente buscado
    """

    id_cliente = id.zfill(10)

    try:
        with open("arquivos_cadastro/cadastro_cliente.txt", 'r') as arquivo:
            for linha in arquivo:
                id_cliente_txt = linha[:10]
                nome_cliente = linha[10:50].strip()
                cpf_cliente = linha[50:61].strip()
                data_nascimento = linha[61:69].strip()
                inf_adicionais = linha[69:].strip()

                if id_cliente == id_cliente_txt:
                    retorno_consulta = {
                        "id_cliente": id_cliente,
                        "nome_cliente": nome_cliente,
                        "cpf_cliente": cpf_cliente,
                        "data_nascimento": data_nascimento,
                        "informacoes": inf_adicionais
                    }
                    return retorno_consulta

            raise ClienteException("Cliente não encontrado")

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de cadastro não encontrado",
        )
    except ClienteException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


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


@app.delete("/delete/cliente/{id}")
def delete_cliente(id: str):
    """
    Deleta um cliente pelo ID.

    Parâmetros:
        - id: ID do cliente a ser deletado.

    Retorna:
        - Uma mensagem de sucesso.

    Exceções:
        - HTTPException: Se ocorrer um erro durante a deleção do cliente.
    """
    id_cliente = id.rjust(10, "0")
    try:
        with open("arquivos_cadastro/cadastro_cliente.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            encontrado = False
            arquivo.seek(0)
            for linha in linhas:
                if linha.startswith(id_cliente):
                    encontrado = True
                    continue
                arquivo.write(linha)
            arquivo.truncate()

        if encontrado:
            return "Sucesso"
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID do cliente não encontrado",
            )

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de cadastro de clientes não encontrado",
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


class FuncoesAuxiliares:

    def calcular_total_pedido(id_produto, qtd_compra):
        """
        Calcula o total do pedido realizado

        Parâmetros:
            - id_produto: ID do produto utilizado no calculo
            - qtd_compra: Quantidade coletada para saber quantos produtos existem na compra

        Retorna:
            - Um dicionário contendo as informações atualizadas do pedido
        """

        id_produto_convertido = str(id_produto)

        with open("arquivos_cadastro/cadastro_produto.txt", "r") as arquivo:
            for linha in arquivo:
                if linha.startswith(id_produto_convertido.zfill(10)):
                    preco_unitario_txt = int(linha[70:80].strip())
                    total_pedido = int(qtd_compra) * preco_unitario_txt
                    descricao_produto_txt = linha[10:60].strip()
                    dict_retorno = {
                        "total_do_pedido": total_pedido,
                        "preco_unitario_txt": preco_unitario_txt,
                        "descricao_produto_txt": descricao_produto_txt,
                    }

                    return dict_retorno

    def escreve_itens_pedido(item: dtos.ItensPedidoDTO):
        """
        Abre o arquivo de cadastro de itens pedido para adicionar as informacoes de vinculo entre item-pedido

        Parâmetros:
            - item: Informações do item de determinado pedido

        Retorna:
            - Uma função que escreve no txt as informações do pedido
        """

        with open("arquivos_cadastro/cadastro_itens_pedido.txt", "a") as arquivo:
            id_produto = item.id_produto.zfill(10)
            id_pedido = item.id_pedido.zfill(10)
            quantidade_comprada = item.quantidade_comprada
            descricao_produto = item.descricao

            informacoes = f"{str(id_produto)}{str(id_pedido)}{str(quantidade_comprada)}{str(descricao_produto)}"
            arquivo.write(f"{informacoes}\n")

    def calcular_novo_estoque(qtd_estoque, qtd_compra: object) -> object:
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
