import os.path
import re 
import random
import datetime 

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
            
def adicionar_informacoes_arquivo(nome_arquivo, id_pedido,cliente_id,pedido_data,status ):
    """
    Adiciona as informações no arquivo TXT. 
    STATUS - POSIÇÃO 41 - 50
    """
    
    status = 'SEPARACAO' 
    with open(nome_arquivo, 'a') as arquivo:    
        pedido_data_sem_barras = pedido_data.replace('/', '')
        informacoes =  f"{id_pedido}{cliente_id}{pedido_data_sem_barras}{status}"
        arquivo.write(f'{informacoes}\n')
        
def cadastro_pedido_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variaveis que devem ser armazenadas
    na ordem correta. 
    """
    verificar_arquivo("cadastro_pedido.txt")
    
    id_pedido = gerar_id_pedido()
    cliente_id = id_cliente()
    pedido_data = data_pedido()
    status = 'SEPARACAO'
    
    adicionar_informacoes_arquivo("arquivos_cadastro/cadastro_pedido.txt", id_pedido,cliente_id,pedido_data, status)
    print(f"ID Pedido: {id_pedido} ID Cliente: {cliente_id} Data do Pedido: {pedido_data} Status: {status}")
        
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
    
def validar_data_pedido(data_pedido):
    """
    Confere se a data do pedido é uma data válida (dd/mm/aaaa).
    """
    try:
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', data_pedido):
            return False
        
        dia, mes, ano = map(int, data_pedido.split('/'))
        
        if not (1 <= dia <= 31 and 1 <= mes <= 12 and ano >= datetime.datetime.now().year and mes >= datetime.datetime.now().month):
            return False
        
        hoje = datetime.datetime.now().date()
        data_formatada = datetime.datetime(ano, mes, dia).date()
        tres_dias_frente = hoje + datetime.timedelta(days=3)
        if hoje <= data_formatada <= tres_dias_frente:
            return True
        else:
            return False
    except ValueError:
        return False

def gerar_id_pedido():
    """
    Gera um código de pedido aleatório. POSIÇÃO 1 - 10
    """
    numero_aleatorio = random.randint(0, 10**5 - 1)
    id_aleatorio = "15221" + str(numero_aleatorio).zfill(5)
    
    return id_aleatorio

def id_cliente():
    """
    Realiza a confirmação se o id do cliente já está cadastrado ou não no TXT. POSIÇÃO 11 - 20
    """
    id_cliente = input("Insira o ID do cliente registrado (10 caracteres): ")
    
    if validar_cliente_id(id_cliente):
        print("Cliente confirmado!")
        return id_cliente
    else:
        print("Cliente não encontrado, certifique-se de cadastrá-lo!")
        exit()
        
def data_pedido():
    """
    Realiza o cadastro da data do pedido baseado no DateTime. - POSIÇÃO 21 - 30
    """
    while True:
        data_pedido = input("Insira a data de cadastro do pedido (dd/mm/aaaa e no máximo 3 dias à frente): ")
        
        if validar_data_pedido(data_pedido):
            print("Cadastro da data realizado!")
            return data_pedido
        else:
            print("Data inválida, certifique-se dela atender a todas as condições!")
            
# def calculo_total(id_pedido,nome_arquivo):
    
#     diretorio = "arquivos_cadastro"
#     if not os.path.exists(diretorio):
#         os.makedirs(diretorio)
        
#     caminho_arquivo = os.path.join(diretorio, nome_arquivo)

#     if not os.path.isfile(caminho_arquivo):
#         with open(caminho_arquivo, 'w'):
#             pass  # Cria o arquivo vazio
    
            
#             with open('cadastro_itens_pedido.txt', 'r') as arquivo:
#                 for linha in arquivo:
#                     teste = linha[:10]
#                     teste == id_pedido
                
#                 if teste ==  id_pedido:
#                     quantidade = int(linha[20:30])
#                     preco_unitario = float(linha[30:35])
                    
#                     total = quantidade * preco_unitario
#                     return total
            
cadastro_pedido_txt