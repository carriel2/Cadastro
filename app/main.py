from fastapi import FastAPI
from controller import cliente_router, pedido_router, estoque_router

app = FastAPI()

app.include_router(cliente_router, prefix="/cliente")
app.include_router(pedido_router, prefix="/pedido")
app.include_router(estoque_router, prefix="/estoque")
