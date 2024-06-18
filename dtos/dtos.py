from pydantic import BaseModel

class ClienteDTO(BaseModel):
    nome:str
    cpf:str
    inf_adicionais:str
    data_nasc:str
    
class PedidoDoProdutoDTO(BaseModel):
    produto_id:str
    quantidade_pedido:int

class PedidoDTO(BaseModel):
    id_cliente:str
    status:str
    data:str
    produtos:list[PedidoDoProdutoDTO]
    
class ProdutoDTO(BaseModel):
    descricao:str
    estoque:str
    preco:str
    
class ItensPedidoDTO(BaseModel):
    descricao:str
    id_produto:str
    id_pedido:str
    quantidade_comprada:int