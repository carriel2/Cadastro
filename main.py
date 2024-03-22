import re

# Função para validar o ID do cliente
def validar_id(id_cliente):
    # Verifica se o ID contém apenas dígitos e tem exatamente 10 caracteres
    return id_cliente.isdigit() and len(id_cliente) == 10

# Função para validar o nome do cliente
def validar_nome(nome):
    # Verifica se o nome contém apenas letras e tem no máximo 40 caracteres
    return bool(re.match("^[a-zA-Z]{1,40}$", nome))

# Função para validar o CPF do cliente
def validar_cpf(cpf_cliente):
    
    cpf_cliente = re.sub(r'[^0-9X]', '' ,cpf_cliente)
    
    if len(cpf_cliente) != 11 and cpf_cliente != 'X':  
        return False

    if cpf_cliente == cpf_cliente[0] * 11:
        return False
    
    return True

# Função para adicionar informações ao arquivo
def adicionar_informacoes_arquivo(nome_arquivo,id_cliente, nome_cliente, cpf_cliente):
    
    id_formatado = id_cliente.zfill(10)
    
    nome_formatado = nome_cliente.ljust(40)
        
    with open(nome_arquivo, 'a') as arquivo:
        arquivo.write(f"{id_formatado}{nome_formatado}{cpf_cliente}\n")
    print("Informação adicionada com sucesso.")

# Função para cadastrar o ID do cliente
def cadastro_id():
    while True:
        id_cliente = input("Insira o ID do cliente que deseja cadastrar: (10 números) ")
        
        if validar_id(id_cliente):
            return id_cliente
        else:
            print("ID inválido")

# Função para cadastrar o cliente
def cadastro_cliente():
    while True:
        nome_cliente = input("Insira o nome do cliente (máximo de 40 letras): ").upper()
        
        if validar_nome(nome_cliente):
            return nome_cliente
        else:
            print("Nome inválido. Por favor, insira um nome com no máximo 40 letras.")
            
def cadastro_cpf():
    while True:
        cpf_cliente = input("Digite o CPF do cliente ")
        cpf_cliente = re.sub(r'[.-]', '', cpf_cliente)
        
        if validar_cpf(cpf_cliente):
            return cpf_cliente
        else:
            print("CPF inválido.")
            
# def cadastro_():
    # while True:

# Função principal para o cadastro completo
def cadastrar_cliente():
    id_cliente = cadastro_id()
    nome_cliente = cadastro_cliente()
    cpf_cliente = cadastro_cpf()
    informacao = f"Cadastro de cliente - {id_cliente}{nome_cliente}{cpf_cliente}"
    adicionar_informacoes_arquivo("exemplo.txt", id_cliente, nome_cliente, cpf_cliente)
    print("Cliente cadastrado:", id_cliente, nome_cliente, cpf_cliente)

# Chamada da função para cadastrar um cliente
cadastrar_cliente()
