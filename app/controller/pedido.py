from fastapi import APIRouter, HTTPException, status
from app.services.pedido import PedidoService
from app.dtos import PedidoDTO, AdicionarItemDTO, AtualizarItemDTO, DeletaItemDTO

router = APIRouter()


@router.post("/cadastrar")
def cadastrar_pedido(body: PedidoDTO):
    try:
        return PedidoService.cadastrar_pedido(body)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/consulta")
def consulta_pedidos():
    try:
        return PedidoService.consulta_pedidos()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/consulta/{id_pedido}")
def consulta_pedido_id(id_pedido: int):
    try:
        return PedidoService.consulta_pedido_id(id_pedido)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/inserir/{id}")
def inserir_item_pedido(id: int, body: AdicionarItemDTO):
    try:
        return PedidoService.inserir_item_pedido(id, body)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/alterar")
def atualizar_item_pedido(body: AtualizarItemDTO):
    try:
        return PedidoService.atualizar_item_pedido(body)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/deleta")
def deleta_item_pedido(body: DeletaItemDTO):
    try:
        return PedidoService.deleta_item_pedido(body)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
