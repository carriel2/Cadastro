from pydantic import BaseModel

class ClienteDTO(BaseModel):
    nome:str
    cpf:str
    inf_adicionais:str
    data_nasc:str
    
class PedidoDTO(BaseModel):
    status:str
    id_cliente:str
    data:str
    
class ProdutoDTO(BaseModel):
    descricao:str
    estoque:str
    preco:str
    