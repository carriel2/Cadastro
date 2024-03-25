import os
import re
import random

# Função para verificar se o arquivo existe e escrever o cabeçalho se necessário
def verificar_arquivo(nome_arquivo):
    diretorio = "arquivos_cadastro"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    if not os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write("CADASTRO PEDIDO\n")

# Função para adicionar as informacoes no arquivo txt
def adicionar_informacoes_arquivo(nome_arquivo, id_armazenado, descricao_armazenada, estoque_armazenado, preco_armazenado):
    with open(nome_arquivo, 'a') as arquivo:
        informacoes = f'{id_armazenado}{descricao_armazenada}{estoque_armazenado}{preco_armazenado}'
        arquivo.write(f'{informacoes}\n')
        
# Função para validar a  descrição do produto
def validar_produto(desc_produto):
    
    return bool(re.match("^[a-zA-Z0-9]{1,50}$", desc_produto))

# Função para validar o estoque de produtos disponivel
def validar_estoque(qtd_estoque):
    qtd_estoque = re.sub(r'[^0-9]', '', qtd_estoque)
    if len(qtd_estoque) <= 10:
        return qtd_estoque
    else:
        print("Quantidade inválida.")
        
def validar_preco(preco):
    preco = re.sub(r'[^0-9,]', '', preco)
    preco_sem_virgula = preco.replace(',', '')
    if preco_sem_virgula and len(preco_sem_virgula) <= 10 and preco_sem_virgula != '0':
        return preco
    else:
        print("Preço inválido.")
        
# Função para gerar de forma aleatória o código do produto
def gerar_id():
    numero_aleatorio = random.randint(0, 10**5 - 1)
    # Adicionar o prefixo "010" ao número gerado
    id_aleatorio = "1122" + str(numero_aleatorio).zfill(5)

    return id_aleatorio

# Função para informar a descrição do produto
def desc_produto():
    while True:
        descricao_produto = input("Insira a descrição do produto (Máx 50 caracteres e sem espaço): ").upper()
        if validar_produto(descricao_produto):
            return descricao_produto
        else:
            print("Insira uma descrição válida!")

#Função para informar quantidade disponivel em estoque
def qtd_estoque():
    while True:
        estoque = input("Insira a quantidade de produtos disponíveis em estoque (Máx 10 caracteres): ")
        if validar_estoque(estoque):
            return estoque
        else:
            print("Insira uma quantidade válida.")
            
# Função para informar o preço unitário do produto            
def preco_unitario():
    while True:
        preco = input("Insira o preço unitário do produto (Máx 10 caracteres): ")
        if validar_preco(preco):
            return preco
        else:
            print("Insira um preço válido.")

# Função para cadastro final dos itens no txt
def cadastrar_pedido():
    verificar_arquivo("cadastro_produto.txt")
    
    id_armazenado = gerar_id()
    descricao_armazenada = desc_produto()
    estoque_armazenado = qtd_estoque()
    preco_armazenado = preco_unitario()
    
    adicionar_informacoes_arquivo("arquivos_cadastro/cadastro_produto.txt", id_armazenado, descricao_armazenada, estoque_armazenado, preco_armazenado)
    print(f"ID:{id_armazenado} Descrição Produto:{descricao_armazenada} Estoque: {estoque_armazenado} Preço Unitário: {preco_armazenado}")
cadastrar_pedido()


