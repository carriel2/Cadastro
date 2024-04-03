import os.path

def verificar_arquivo(nome_arquivo):
    """
    Verifica se o arquivo existe e escreve o cabeçalho se necessário.
    """
    diretorio = "arquivos_cadastro"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    if not os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write("CADASTRO ITENS PEDIDO\n")

def adicionar_informacoes_arquivo(nome_arquivo, pedido_id, produto_id, quantidade,preco_unitario):
    """
    Adiciona as informações ao arquivo.
    """
    with open(nome_arquivo, 'a') as arquivo:
        informacoes = f'{pedido_id}{produto_id}{quantidade}{preco_unitario}'
        arquivo.write(f'{informacoes}\n')

def cadastro_itens_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variáveis que devem ser armazenadas
    na ordem correta. 
    """
    verificar_arquivo("cadastro_itens_pedido.txt")
    pedido_id = id_pedido()
    produto_id = id_produto()
    preco_unitario = importa_preco_unitario(produto_id)
    quantidade = quantidade_compra()
    
    adicionar_informacoes_arquivo("arquivos_cadastro/cadastro_itens_pedido.txt", pedido_id, produto_id, quantidade,preco_unitario)
    print(f"ID Pedido: {pedido_id} ID Produto: {produto_id} Quantidade: {quantidade} Preço Unitário: {preco_unitario}")
    
def validar_numero_pedido(id_pedido):
    """
    Confere se o ID do pedido já está registrado.
    """
    with open('arquivos_cadastro/cadastro_pedido.txt', 'r') as arquivo:
        for linha in arquivo:
            pedido_id = linha[:10].strip()
            if pedido_id == id_pedido:
                return True
    return False

def validar_id_produto(id_produto):
    """
    Confere se o ID do produto já está registrado.
    """
    with open("arquivos_cadastro/cadastro_produto.txt", 'r') as arquivo:
        for linha in arquivo:
            produto_id = linha[:10].strip()
            if produto_id == id_produto:
                return True
    return False

def validar_quantidade(quantidade_compra):
    """
    Valida a quantidade de itens inseridos para compra.
    """
    try:
        quantidade_compra = str(quantidade_compra) 
        if quantidade_compra.isdigit() and len(quantidade_compra) <= 10:
            quantidade_compra = int(quantidade_compra)
            if quantidade_compra > 0:
                return quantidade_compra
    except ValueError:
        pass
    
    print("Quantidade inválida. Insira somente números inteiros com até 10 caracteres.")
    return None 

def importa_preco_unitario(produto_id):
    """
    Importa o preço unitário do produto baseado no ID do produto fornecido.
    """
    with open("arquivos_cadastro/cadastro_produto.txt", 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith(produto_id):
                preco_unitario = linha.strip()[70:].strip() 
                if preco_unitario:
                    return float(preco_unitario)
    return None
    
def id_pedido():
    """ 
    Verifica se o ID inserido pelo usuário está cadastrado no TXT
    com auxilio da função validadora.
    """
    id_pedido = input("Insira o ID do pedido cadastrado (10 caracteres): ")
    if validar_numero_pedido(id_pedido):
        print("ID encontrado!")
        return id_pedido
    else:
        print("ID não registrado ou inválido.")
        exit()

def id_produto():
    """
    Verifica se o ID inserido pelo usuário está cadastrado no TXT
    com auxilio da função validadora.
    """
    id_produto = input("Insira o ID do produto cadastrado (10 caracteres): ")        
    if validar_id_produto(id_produto):
        print ("ID encontrado!")
        return id_produto
    else: 
        print("ID não registrado ou inválido.")
        exit()

def quantidade_compra():
    """
    Função para o usuário inserir a quantidade de produtos
    que deseja comprar.
    """
    while True:
        quantidade_compra = input("Insira a quantidade de produtos que deseja comprar: (Máx 10 caracteres): ")
        quantidade_compra = quantidade_compra.zfill(10)
        if validar_quantidade(quantidade_compra):
            print("Quantidade registrada!")
            return quantidade_compra

def calculo_total(quantidade, preco_unitario):
    
    quantidade = int(quantidade)
    preco_unitario = float(preco_unitario)
    total_pedido = preco_unitario * quantidade
    
    return total_pedido

cadastro_itens_txt

