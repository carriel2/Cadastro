from cadastros.cadastro_cliente import cadastro_cliente_txt
from cadastros.cadastro_produto import cadastro_produto_txt
from cadastros.cadastro_pedido import cadastro_pedido_txt
from cadastros.cadastro_itens_pedido import cadastro_itens_txt

def cabecalho():
    """
    INTERFACE USUÁRIO E ESCOLHAS
    """
    largura = 30
    texto = 'Bem Vindo a PedralhaERP'
    text_center = texto.center(largura)

    print('-' * 30)
    print(text_center)
    print('-' * 30)

    largura = 30
    menu = 'MENU'
    texto = ' 1 - Cadastrar Cliente \n 2 - Cadastrar Produto \n 3 - Cadastrar Pedido \n 4 - Cadastrar itens no Pedido \n 5 - Consultar Clientes \n 6 - Consultar Produtos \n 7 - Consultar Pedidos \n 8 - Preço Pedidos '       
    text_center = menu.center(largura)

    print('-' * 30)
    print(text_center)
    print('-' * 30)
    print(texto)

    escolha = input("Escolha uma das opções do menu: ")

    direcionar_menu(escolha)

def direcionar_menu(escolha):
    """
    Função para redirecionar o usuário de acordo com a escolha dele
    para determinado menu.
    """
    opcoes_menu = {
        '1': menu_cadastro_cliente,
        '2': menu_cadastro_produto,
        '3': menu_cadastro_pedido,
        '4': menu_cadastrar_itens_pedido,
        '5': menu_consultar_clientes,
        '6': menu_consultar_produtos,
        '7': menu_consultar_pedidos,
        '8': menu_total_pedidos
    }
    
    funcao_menu = opcoes_menu.get(escolha)
    
    if funcao_menu:
        funcao_menu()
    else:
        print("Escolha inválida.")

def menu_cadastro_cliente():
    """
    Função que acessa a função de cadastro do cliente,
    fazendo com que o usuário cadastre o cliente no TXT.
    """
    
    print('-' * 30)
    print('Você está no menu de cadastro de clientes')
    print('-' * 30)
    
    cadastro_cliente_txt()
    
    escolha = input("Digite o número da escolha desejada: \n (1- CADASTRO CLIENTE / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
    while escolha != '3':
        if escolha == '1':
            menu_cadastro_cliente()
        elif escolha == '2':
            cabecalho()
        else:
            print('Insira uma escolha válida!')
        escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO CLIENTE / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
            
    exit()

def menu_cadastro_produto():
    """
    Função que acessa a função de cadastro do produto,
    fazendo com que o usuário cadastre o produto no TXT.
    """
    
    print('-' * 30)
    print('Você está no menu de cadastro de produtos')
    print('-' * 30)
    
    cadastro_produto_txt()
    
    escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PRODUTO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
    while escolha != '3':
        if escolha == '1':
            menu_cadastro_produto()
        elif escolha == '2':
            cabecalho()
        else:
            print('Insira uma escolha válida!')
        escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PRODUTO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
            
    exit()

def menu_cadastro_pedido():
    """
    Função que acessa a função de cadastro do pedido,
    fazendo com que o usuário cadastre o pedido no TXT.
    """
    
    print('-' * 30)
    print('Você está no menu de cadastro de pedidos')
    print('-' * 30)
    
    cadastro_pedido_txt()
    
    escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR)")
    
    while escolha != '3':
        if escolha == '1':
            menu_cadastro_pedido()
        elif escolha == '2':
            cabecalho()
        else:
            print('Insira uma escolha válida!')
        escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
            
    exit()

def menu_cadastrar_itens_pedido():
    """
    Função que acessa a função de cadastro dos itens do pedido,
    fazendo com que o usuário cadastre os itens no pedido.
    """
    
    print('-' * 30)
    print('Você está no menu de cadastro de itens do pedido')
    print('-' * 30)
    
    cadastro_itens_txt() 
    
    escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO ITEM / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
    while escolha != '3':
        if escolha == '1':
            menu_cadastrar_itens_pedido()
        elif escolha == '2':
            cabecalho()
        else:
            print('Insira uma escolha válida!')
        escolha = input("Digite o número da escolha desejada: \n (1- CADASTRO OUTRO ITEM / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
            
    exit()
    
def menu_consultar_clientes():
    """
    Função que acessa a função de consulta de clientes,
    fazendo com que o usuário consiga consultar os clientes cadastrados.
    """
    
    print('-' * 30)
    print('Você está no menu de consulta de clientes')
    print('-' * 30)
    
    consultar_clientes()
    
    escolha = input("Digite o número da escolha desejada: \n (1- CONSULTAR OUTRO CLIENTE / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
    while escolha != '3':
        if escolha == '1':
            menu_consultar_clientes()
        elif escolha == '2':
            cabecalho()
        else:
            print("Insira uma escolha válida")
        escolha = input("Digite o número da escolha desejada: \n (1- CONSULTAR OUTRO CLIENTE / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    exit()
    
def menu_consultar_produtos():
    """
    Função que acessa a função de consulta de produtos,
    fazendo com que o usuário consiga consultar os produtos cadastrados.
    """
    
    print('-' * 30)
    print('Você está no menu de consulta de produtos')
    print('-' * 30)
    
    consultar_produtos()
    
    escolha = input("Digite o número da escolha desejada: \n (1- CONSULTAR OUTRO PRODUTO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
    while escolha != '3':
        if escolha == '1':
            menu_consultar_produtos()
        elif escolha == '2':
            cabecalho()
        else:
            print("Insira uma escolha válida")
        escolha = input("Digite o número da escolha desejada: \n (1- CONSULTAR OUTRO PRODUTO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    exit()
    
def menu_consultar_pedidos():    
    """
    Função que acessa a função de consulta de pedidos,
    fazendo com que o usuário consiga consultar os pedidos cadastrados.
    """
    print('-' * 30)
    print('Você está no menu de consulta de pedidos')
    print('-' * 30)
    
    consultar_pedidos()
    
    escolha = input("Digite o número da escolha desejada: \n (1- CONSULTAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
    while escolha != '3':
        if escolha == '1':
            menu_consultar_pedidos
        elif escolha == '2':
            cabecalho()
        else:
            print("Insira uma escolha válida")
        escolha = input("Digite o número da escolha desejada: \n (1- CONSULTAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR ")
    exit()

def menu_total_pedidos():
    """
    Calcula o total dos pedidos.
    """
    try:
        with open("arquivos_cadastro/cadastro_itens_pedido.txt", 'r') as arquivo:
            next(arquivo)
            for linha in arquivo:   
                preco = linha[30:].strip()
                quantidade = linha[20:30].strip()
                id_pedido = linha[0:10].strip()
                total = int(quantidade) * float(preco)
                
                print(f"ID do pedido: {id_pedido} -- Total do Pedido: {total}")
    except FileNotFoundError:
        print("Nenhum produto cadastrado.")
        
    exit()
    
def consultar_clientes_txt():
    """
    Consulta os clientes cadastrados no TXT.
    """
    try:
        with open("arquivos_cadastro/cadastro_cliente.txt", 'r') as arquivo:
            clientes = []
            next(arquivo)
            for linha in arquivo:
                id_cliente = linha[:10].strip()
                nome = linha[10:40].strip()
                cpf = linha[40:61].strip()
                clientes.append({'id': id_cliente, 'nome': nome, 'cpf': cpf})
            if not clientes:
                print("Nenhum cliente cadastrado.")
            return clientes
    except FileNotFoundError:
        print("Nenhum cliente cadastrado.")
        return []

def formatar_cliente(cliente):
    """
    Formata os clientes para exibição.
    """
    return f"ID: {cliente['id']}, Nome: {cliente['nome']}, CPF: {cliente['cpf']}"

def consultar_clientes():
    """
    Consulta e exibe os clientes cadastrados.
    """
    clientes = consultar_clientes_txt() 
    if clientes: 
        print("Clientes Cadastrados:")
        for cliente in clientes:
            print(formatar_cliente(cliente))
    else:
        exit()

def consultar_produtos_txt():
    """
    Consulta os produtos cadastrados no arquivo TXT.
    """
    try:
        with open("arquivos_cadastro/cadastro_produto.txt", 'r') as arquivo:
            produtos = []
            next(arquivo)
            for linha in arquivo:
                id_produto = linha[:10].strip()
                nome_produto = linha[10:60].strip().replace('_', '')
                quantidade_estoque = linha[60:70].strip().replace('_', '')
                preco_unitario = linha[70:].strip()
                produtos.append({'id': id_produto, 'nome': nome_produto, 'quantidade': quantidade_estoque, 'preco': preco_unitario})
            if not produtos:
                print("Nenhum produto cadastrado.")
            return produtos
    except FileNotFoundError:
        print("Nenhum produto cadastrado.")
        return []

def formatar_produto(produto):
    """
    Formata os produtos para exibição.
    """
    return f"ID: {produto['id']}, Nome: {produto['nome']}, Quantidade em Estoque: {produto['quantidade']}, Preço Unitário: R$ {produto['preco']}"

def consultar_produtos():
    """
    Consulta e exibe os produtos cadastrados.
    """
    produtos = consultar_produtos_txt()
    if produtos:
        print("Produtos Cadastrados:")
        for produto in produtos:
            if produto['id']:   
                print(formatar_produto(produto))
    else:
        exit()  
            
def consultar_pedidos_txt():
    """
    Consulta os pedidos cadastrados no arquivo TXT.
    """

    try:
        with open("arquivos_cadastro/cadastro_pedido.txt", 'r') as arquivo:
            pedidos = []
            next(arquivo)
            for linha in arquivo:
                id_pedido = linha[:10].strip()
                id_cliente = linha[10:20].strip()
                data_pedido = linha[20:28].strip()
                pedido_status = linha[28:].strip() 
                pedidos.append({'id_pedido': id_pedido, 'id_cliente': id_cliente, 'data_pedido': data_pedido, 'pedido_status': pedido_status})
            if not pedidos:
                    print("Nenhum pedido cadastrado.")
            return pedidos
    except FileNotFoundError:
        print("Nenhum pedido cadastrado.")
    return []
 
def formatar_pedido(pedido):
    """
    Formata os pedidos para exibição.
    """
    

        
    
    id_pedido = pedido['id_pedido']
    id_cliente = pedido['id_cliente']
    data_pedido = pedido['data_pedido']
    data_formatada = f"{data_pedido[0:2]}/{data_pedido[2:4]}/{data_pedido[4:]}"
    pedido_status = pedido['pedido_status']
    
    with open("arquivos_cadastro/cadastro_itens_pedido.txt", 'r') as arquivo:
        next(arquivo)
    for linha in arquivo:
        if linha[:10] == id_pedido:
            menu_total_pedidos()
    if id_pedido:
        return f"ID Pedido: {id_pedido}, ID Cliente: {id_cliente}, Data do Pedido: {data_formatada}, Status do Pedido: {pedido_status}, Valor{} "
    else:
        return None
            
def consultar_pedidos():
    """
    Consulta e exibe os pedidos cadastrados.
    """
    pedidos = consultar_pedidos_txt()
    if pedidos:
        print("Pedidos Cadastrados:")
        for pedido in pedidos:
            pedido_formatado = formatar_pedido(pedido)
            if pedido_formatado:
                print(pedido_formatado)
    else:
        exit()
        
cabecalho()