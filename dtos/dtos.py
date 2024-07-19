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
    novo_status: Optional[str] = None


class ItensPedidoDTO(BaseModel):
    id_pedido: str
    id_produto: str
    quantidade_comprada: int


class AdicionarItemDTO(BaseModel):
    id_produto: int
    quantidade_comprada: int


class AtualizarItemDTO(BaseModel):
    id_produto: int
    id_pedido: int
    quantidade_comprada: int


class DeletaEstoqueDTO(BaseModel):
    id_pedido: int
    id_produto: int


class DeletaItemDTO(BaseModel):
    id_produto: int
    id_pedido: int


class AtualizaClienteDTO(BaseModel):
    nome: str
    data_nasc: str
    inf_adicionais: str
