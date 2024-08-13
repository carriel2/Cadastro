from .cliente import router as cliente_router
from .pedido import router as pedido_router
from .estoque import router as estoque_router

__all__ = ["cliente_router", "pedido_router", "estoque_router"]
