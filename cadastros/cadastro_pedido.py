import os
import re 
import random

def verificar_arquivo(nome_arquivo):
    """
    Verifica se o arquivo existe e cria o cabeçalho se necessário.
    """
    diretorio = "arquivos_cadastro"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    if not os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write("CADASTRO PEDIDO\n")
            
def adicionar_informacoes_arquivo(nome_arquivo, id_pedido,cliente_id ):
    """
    Adiciona as informações no arquivo TXT.
    """
    with open(nome_arquivo, 'a') as arquivo:
        informacoes =  f"{id_pedido}{cliente_id}"
        arquivo.write(f'{informacoes}\n')
        
def validar_cliente_id(id_cliente):
    """
    Confere se o cliente está cadastrado
    """
    with open('arquivos_cadastro/cadastro_cliente.txt', 'r') as arquivo:
        for linha in arquivo:
            cliente_id = linha[:10].strip()
            if cliente_id == id_cliente:
                return True
            
    return False
    
def gerar_id_pedido():
    """
    Gera um código de pedido aleatório.
    """
    numero_aleatorio = random.randint(0, 10**4 - 1)
    id_aleatorio = "15221" + str(numero_aleatorio).zfill(4)
    
    return id_aleatorio

def id_cliente():
    
    id_cliente = input("Insira o ID do cliente registrado (Máx 10 caracteres) ")
    
    if validar_cliente_id(id_cliente):
        print("Cliente confirmado!")
        return id_cliente
    else:
        print("Cliente não encontrado, certifique-se de cadastrá-lo!")

def cadastrar_pedido():
    """
    Realiza o cadastro completo do pedido
    """
    verificar_arquivo("cadastro_pedido.txt")
    
    id_pedido = gerar_id_pedido()
    cliente_id = id_cliente()
    

    adicionar_informacoes_arquivo("arquivos_cadastro/cadastro_pedido.txt", id_pedido,cliente_id)
    print(f"ID Pedido: {id_pedido} ID Cliente: {cliente_id}")
     
cadastrar_pedido()