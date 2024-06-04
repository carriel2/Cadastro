from fastapi import FastAPI, HTTPException, status
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
    verificar_arquivo,
    id_cliente,
)
from exceptions.exceptions import (
    CPFException,
    ClienteException,
    DataException,
    NomeInvalido,
    ProdutoException,
)
import dtos.dtos as dtos
import os

app = FastAPI()


@app.post("/cadastrar/pedido")
def create_pedido(body: dtos.PedidoDTO):
    """
    Cadastra um novo pedido.

    Args:
        body: Objeto PedidoDTO contendo as informações do pedido.

    Retorna:
        - Objeto PedidoDTO do pedido cadastrado.

    Lança:
        - HTTPException: Se ocorrer um erro durante o cadastro do pedido.
    """
    try:
        verificar_arquivo("cadastro_pedido.txt")

        id_pedido = proximo_sequencial("arquivos_cadastro/cadastro_pedido.txt")
        cliente_id = id_cliente(body.id_cliente)
        situacao = body.status
        data = body.data

        validar_data_pedido(data)
        adicionar_informacoes_arquivo(
            "arquivos_cadastro/cadastro_pedido.txt",
            id_pedido,
            cliente_id,
            data,
            situacao,
        )
        return body

    except ClienteException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Formato de data inserido é inválido.",
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

    """
    Consulta todos os clientes cadastrados.

    Retorna:
        - Uma lista de clientes formatados.
    """
    diretorio = "arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_cliente.txt")
    formatar_funcao = Consultas.formatar_cliente

    return Consultas.consultar_arquivo(caminho_arquivo, formatar_funcao)


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


@app.put("/alterar/produto/{id}")   
def update_produtos(id: str, body: dtos.ProdutoDTO):
    id_produto = id.zfill(10)

    try:
        encontrado = False
        produtos_atualizados = []

        with open("arquivos_cadastro/cadastro_produto.txt", "r") as arquivo:
            primeira_linha = arquivo.readline()
            for linha in arquivo:
                if linha.startswith(id_produto):
                    encontrado = True
                    nova_desc = body.descricao
                    novo_estoque = body.estoque
                    novo_preco = body.preco

                    validar_produto(nova_desc)
                    validar_estoque(novo_estoque)
                    validar_preco(novo_preco)

                    linha_atualizada = (
                        str(id_produto)
                        + nova_desc.ljust(50)
                        + novo_estoque.ljust(10)
                        + novo_preco
                        + "\n"
                    )
                    produtos_atualizados.append(linha_atualizada)
                else:
                    produtos_atualizados.append(linha)

        if not encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
            )

        with open("arquivos_cadastro/cadastro_produto.txt", "w") as arquivo:
            arquivo.write(primeira_linha)
            arquivo.writelines(produtos_atualizados)

        return body

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
def delete_produto(id:str):
    
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

        adicionar_informacoes_arquivo_2(
            "arquivos_cadastro/cadastro_cliente.txt",
            cliente_id,
            nome_cliente,
            cpf_cliente,
            inf_adc,
            data_nasc,
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
