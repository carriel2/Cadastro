from fastapi import APIRouter, HTTPException, status
from app.database.db_connection import get_connection
from app.services.cliente import ClienteService
from app.dtos import ClienteDTO, AtualizaClienteDTO

router = APIRouter()


@router.post("/cadastrar")

def create_cliente(body: ClienteDTO):
    """
    Cadastra um novo cliente no Sistema e banco de dados.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ClienteService.create_cliente(body, cursor)
        conn.commit()
        return "Sucesso"
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()
        cursor.close()


@router.get("/consulta")
def consulta_clientes():
    """
    Consulta todos os clientes cadastrados na base de dados.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        return ClienteService.consulta_clientes(cursor)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()
        cursor.close()


@router.get("/consulta/{cpf}")
def consulta_cliente_cpf(cpf: str):
    """
    Consulta um cliente específico baseado no CPF inserido na URL.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        return ClienteService.consulta_cliente_cpf(cpf, cursor)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()
        cursor.close()


@router.put("/atualiza/{id}")
def atualizar_cliente(id: str, body: AtualizaClienteDTO):
    """
    Atualiza os dados cadastrais de um cliente de acordo com o id fornecido na URL.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ClienteService.atualizar_cliente(id, body, cursor)
        conn.commit()
        return "Sucesso"
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/deleta/{cpf}")
def deleta_cliente(cpf: str):
    """
    Deleta um cliente pelo CPF inserido na URL.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        ClienteService.deleta_cliente(cpf, cursor)
        conn.commit()
        return {"details": "Sucesso", "CPF": cpf}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        cursor.close()
        conn.close()
