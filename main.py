from fastapi import FastAPI, HTTPException, status

from cadastros.cadastro_cliente import adicionar_informacoes_arquivo, cadastro_id, verificar_arquivo
from consultas.consulta_pedido import Consultas

import dtos

import os

app = FastAPI()

@app.get("/consulta/pedido")
def get_pedidos():
    diretorio = "arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_pedido.txt")
    formatar_funcao = Consultas.formatar_pedido
    
    return Consultas.consultar_arquivo(caminho_arquivo, formatar_funcao)
    
@app.get("/consulta/cliente")
def get_clientes():
    diretorio ="arquivos_cadastro"
    caminho_arquivo = os.path.join(diretorio, "cadastro_cliente.txt")
    formatar_funcao = Consultas.formatar_cliente
    
    return Consultas.consultar_arquivo(caminho_arquivo, formatar_funcao)

@app.post("/cadastrar/cliente")
def create_cliente(body:dtos.ClienteDTO):
    
    verificar_arquivo("cadastro_cliente.txt")

    id_cliente = cadastro_id()
    nome_cliente = body.nome
    cpf_cliente = body.cpf
    data_nasc = body.data_nasc
    infos_adc = body.inf_adicionais

    adicionar_informacoes_arquivo(
        "arquivos_cadastro/cadastro_cliente.txt",
        id_cliente,
        nome_cliente,
        cpf_cliente,
        data_nasc,
        infos_adc,
    ) 
    
    return body

@app.put("/alterar/cliente/{id}")
def update_cliente(id:str,body:dtos.ClienteDTO):
    
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
                    
                    if len(novo_nome) > 40:
                       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Nome Excede o limite de 40 caracteres")

                    if (
                        len(novo_cpf) != 11
                        or not novo_cpf[:-1].isdigit()
                        or (novo_cpf[-1] not in "0123456789X")
                    ):
                       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insira um formato de CPF Válido")

                    if (
                        len(nova_data_nascimento) != 10
                        or not nova_data_nascimento.replace("/", "").isdigit()
                    ):
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insira um formato de data válido")

                    if len(info_adicionais) > 30:
                       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informações adicionais excede o limite de 30 caracteres")

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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não Encontrado")

            with open("arquivos_cadastro/cadastro_cliente.txt", "w") as arquivo:
                arquivo.writelines(clientes_atualizados)

            return body
        
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo de cadastro não encontrado")
    except HTTPException as e:
        raise e
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
   
@app.delete("/delete/cliente/{id}")
def delete_cliente(id:str):
        
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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID do cliente não encontrado")

        except FileNotFoundError:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo de cadastro de clientes não encontrado")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
        
        