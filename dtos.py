from pydantic import BaseModel

class ClienteDTO(BaseModel):
    nome:str
    cpf:str
    inf_adicionais:str
    data_nasc:str