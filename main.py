from cadastros.cadastro_cliente import cadastro_cliente_txt
from cadastros.cadastro_produto import cadastro_produto_txt
from cadastros.cadastro_pedido import cadastro_pedido_txt
from cadastros.cadastro_itens_pedido import cadastro_itens_txt
from cadastros.cadastro_itens_pedido import verificar_arquivo

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
    texto = ' 1 - Cadastrar Cliente \n 2 - Cadastrar Produto \n 3 - Cadastrar Pedido \n 4 - Cadastrar itens no Pedido \n 5 - Consultar Clientes \n 6 - Consultar Produtos \n 7 - Consultar Pedidos'       
    text_center = menu.center(largura)

    print('-' * 30)
    print(text_center)
    print('-' * 30)
    print(texto)

    escolha = input("Escolha uma das opções do menu: ")

    direcionar_menu(escolha)

def direcionar_menu(escolha):
    opcoes_menu = {
        '1': menu_cadastro_cliente,
        '2': menu_cadastro_produto,
        '3': menu_cadastro_pedido,
        '4': menu_cadastrar_itens_pedido,
        '5': menu_consultar_clientes,
        '6': menu_consultar_produtos,
        '7': menu_consultar_pedidos,
    }
    
    funcao_menu = opcoes_menu.get(escolha)
    
    if funcao_menu:
        funcao_menu()
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
        cabecalho()

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

def verificar_disponibilidade_estoque(id_produto, quantidade_solicitada):
    """
    Verifica se há estoque suficiente para o produto especificado.
    Retorna True se houver estoque suficiente, False caso contrário.
    """
    with open("arquivos_cadastro/cadastro_produto.txt", 'r') as arquivo:
        next(arquivo) 
        for linha in arquivo:
            id_produto_arquivo = linha[:10].strip()
            if id_produto_arquivo == id_produto:
                quantidade_estoque = int(linha[60:70].strip())
                return quantidade_estoque >= quantidade_solicitada
    return False

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
    
    escolha = input("Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) ")
    
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
    
    escolha = input("Escolha uma das opções: \n (1- VER TODOS OS PEDIDOS / 2- VER PEDIDO PELO ID / 3- RETORNAR PARA ESCOLHAS / 4- SAIR) ")
    
    while escolha != '4':
        if escolha == '1':
            consultar_pedidos_geral()
        elif escolha == '2':
            consultar_pedido_por_id()
        elif escolha == '3':
            cabecalho()
        else:
            print("Insira uma escolha válida")
        escolha = input("Escolha uma das opções: \n (1- VER TODOS OS PEDIDOS / 2- VER PEDIDO PELO ID / 3- RETORNAR PARA ESCOLHAS / 4- SAIR) ")
        
        
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
                
                return clientes
            
            if not clientes:
                print("Nenhum Cliente Cadastrado.")
                
                escolha = input("Deseja cadastrar um novo cliente  (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
                while escolha != '3':
                    if escolha == '1':
                        cadastro_cliente_txt()
                    elif escolha == '2':
                        cabecalho()
                    else:
                        print("Insira uma escolha válida")
                        escolha = input("Deseja cadastrar um novo cliente? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
                        
                exit()
                
    except FileNotFoundError:
        print("Arquivo não encontrado, realizando criação...")
        verificar_arquivo(nome_arquivo="cadastro_cliente.txt")
        escolha = input("Arquivo Criado! Já que está vazio, deseja cadastrar um novo cliente? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
        while escolha != '3':
            if escolha == '1':
                cadastro_produto_txt()
            elif escolha == '2':
                cabecalho()
            else:
                print("Insira uma escolha válida")
            escolha = input("Deseja cadastrar um cliente? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
            
        exit()
        
    return[]

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
                
                return produtos
            
            if not produtos:
                print("Nenhum produto cadastrado.")
                
                escolha = input("Deseja cadastrar um novo produto? (1- Sim / 2- Voltar ao Menu / 3- Sair) ")
                while escolha != '3':
                    if escolha == '1':
                        cadastro_produto_txt()
                    elif escolha == '2':
                        cabecalho()
                    else:
                        print("Insira uma escolha válida")
                    escolha = input("Deseja cadastrar um novo produto? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
                    
                exit()

    except FileNotFoundError:
        print("Arquivo não encontrado, realizando criação.")
        verificar_arquivo(nome_arquivo="cadastro_produto.txt")
        escolha = input("Arquivo Criado! Já que está vazio, deseja cadastrar um novo produto? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
        while escolha != '3':
            if escolha == '1':
                cadastro_produto_txt()
            elif escolha == '2':
                cabecalho()
            else:
                print("Insira uma escolha válida")
            escolha = input("Deseja cadastrar um novo produto? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
            
        exit()
        
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
                return pedidos
            
            if not pedidos:
                    print("Nenhum pedido cadastrado.")
 
                    escolha = input("Deseja cadastrar um novo pedido? (1- Sim / 2- Voltar ao Menu / 3- Sair) ")
                    while escolha != '3':
                        if escolha == '1':
                            cadastro_produto_txt()
                        elif escolha == '2':
                            cabecalho()
                        else:
                            print("Insira uma escolha válida")
                        escolha = input("Deseja cadastrar um novo pedido? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
                        
                    exit()
                    
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando novo arquivo...")
        verificar_arquivo(nome_arquivo="cadastro_pedido.txt")
        escolha = input("Arquivo Criado! Já que está vazio, deseja cadastrar um novo pedido? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
        while escolha != '3':
            if escolha == '1':
                cadastro_pedido_txt()
            elif escolha == '2':
                cabecalho()
            else:
                print("Insira uma escolha válida")
            escolha = input("Deseja cadastrar um novo pedido? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
            
        exit()
 
def formatar_pedido(pedido):
    """
    Formata os pedidos para exibição.
    """
    id_pedido = pedido['id_pedido']
    id_cliente = pedido['id_cliente']
    data_pedido = pedido['data_pedido']
    data_formatada = f"{data_pedido[0:2]}/{data_pedido[2:4]}/{data_pedido[4:]}"
    pedido_status = pedido['pedido_status']
    
    return f"ID Pedido: {id_pedido}, ID Cliente: {id_cliente}, Data do Pedido: {data_formatada}, Status do Pedido: {pedido_status}, Valor Total: "

def calcular_total_pedido(id_pedido):
    """
    Calcula o valor total do pedido com base nos itens do pedido.
    """
    total = 0
    
    with open("arquivos_cadastro/cadastro_itens_pedido.txt", 'r') as arquivo:
        next(arquivo) 
        for linha in arquivo:
            id_pedido_linha = linha[:10].strip()
            if id_pedido == id_pedido_linha:
                preco_str = linha[30:].strip()
                if preco_str:
                    preco = float(preco_str)
                    quantidade = int(linha[20:30].strip())
                    total += preco * quantidade
                    
    return total

def consultar_pedidos_geral():
    """
    Consulta e exibe todos os pedidos cadastrados.
    """
    pedidos = consultar_pedidos_txt()
    if pedidos:
        print("Pedidos Cadastrados:")
        for pedido in pedidos:
            id_pedido = pedido['id_pedido']
            id_cliente = pedido['id_cliente']
            data_pedido = pedido['data_pedido']
            data_formatada = f"{data_pedido[0:2]}/{data_pedido[2:4]}/{data_pedido[4:]}"
            pedido_status = pedido['pedido_status']
            
            total_pedido = calcular_total_pedido(id_pedido)
            
            print(f"ID Pedido: {id_pedido}, ID Cliente: {id_cliente}, Data do Pedido: {data_formatada}, Status do Pedido: {pedido_status}, Valor Total: R${total_pedido}")
    else:
        
        exit()

def consultar_pedido_por_id():
    """
    Consulta e exibe os pedidos com base no ID.
    """
    buscar = input("Insira o ID do pedido que deseja visualizar: ")

    try:
        with open("arquivos_cadastro/cadastro_pedido.txt", 'r') as arquivo:
            for linha in arquivo:
                id_pedido = linha[:10].strip()
                id_cliente = linha[10:20].strip()
                data_pedido = linha[20:28].strip()
                pedido_status = linha[28:].strip()
                if id_pedido == buscar:
                    total_pedido = calcular_total_pedido(id_pedido)
                    data_formatada = f"{data_pedido[0:2]}/{data_pedido[2:4]}/{data_pedido[4:]}"
                    print(f"ID Pedido: {id_pedido}, ID Cliente: {id_cliente}, Data do Pedido: {data_formatada}, Status do Pedido: {pedido_status}, Valor Total: R${total_pedido}")
                    break
            else:
                print("Pedido não encontrado.")
                return
            
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando novo arquivo...")
        verificar_arquivo(nome_arquivo="arquivos_cadastro/cadastro_pedido.txt")
        escolha = input("Arquivo Criado! Já que está vazio, deseja cadastrar um novo pedido? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
        while escolha != '3':
            if escolha == '1':
                cadastro_pedido_txt()
            elif escolha == '2':
                cabecalho()
            else:
                print("Insira uma escolha válida")
            escolha = input("Deseja cadastrar um novo pedido? (1- Sim/ 2- Voltar ao Menu / 3- Sair) ")
            
        exit()

    escolha = input("O que deseja fazer?\n(1- CONSULTAR OUTRO PEDIDO / 2- RETORNAR PARA O MENU INICIAL / 3 - SAIR) ")

    while escolha != '3':
        if escolha == '1':
            menu_consultar_pedidos()
        elif escolha == '2':
            cabecalho()
        else:
            print("Insira uma escolha válida")
        escolha = input("Escolha uma das opções:\n(1- CONSULTAR OUTRO PEDIDO / 2- RETORNAR PARA O MENU INICIAL / 3 - SAIR) ")
        
    exit()
 
cabecalho()