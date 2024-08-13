from fastapi import APIRouter, HTTPException, status
from app.services.estoque import EstoqueService
from app.dtos import EstoqueDTO

router = APIRouter()


@router.post("/cadastrar/")
def cadastrar_estoque(body: EstoqueDTO):
    try:
        return EstoqueService.cadastrar_estoque(body)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/consulta/")
def consultar_estoque():
    try:
        return EstoqueService.consultar_estoque()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/consulta/{id}")
def consultar_estoque_id(id: str):
    try:
        return EstoqueService.consultar_estoque_id(id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/atualiza/{id}")
def atualiza_estoque(id: int, body: EstoqueDTO):
    try:
        return EstoqueService.atualiza_estoque(id, body)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/deleta/{id}")
def deleta_produto_estoque(id: int):
    try:
        return EstoqueService.deleta_produto_estoque(id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
