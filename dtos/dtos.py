from typing import Optional
from pydantic import BaseModel


class ClienteDTO(BaseModel):
    nome: str
    cpf: str
    inf_adicionais: Optional[str] = None
    data_nasc: str


class PedidoDoProdutoDTO(BaseModel):
    produto_id: int
    quantidade_pedido: int


class PedidoDTO(BaseModel):
    id_cliente: str
    status: str
    data: str
    produtos: list[PedidoDoProdutoDTO]


class EstoqueDTO(BaseModel):
    nome_produto: str
    estoque: str
    preco: float


class UpdatePedidoDTO(BaseModel):
    id_cliente: str
    id_pedido: str
    id_novo_produto: Optional[list] = None
    novo_valortotal: Optional[float] = None
    novo_status:  Optional[str] = None


class ItensPedidoDTO(BaseModel):
    id_pedido: str
    id_produto: str
    quantidade_comprada: int
