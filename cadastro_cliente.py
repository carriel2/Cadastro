import re
import os.path

# Função para validar o nome do cliente
def validar_nome(nome):
    return bool(re.match("^[a-zA-Z]{1,40}$", nome))

# Função para validar o CPF do cliente e verificar se já existe no arquivo
def validar_cpf(cpf_cliente):
    cpf_cliente = re.sub(r'[^0-9X]', '', cpf_cliente)
    
    # Verificar se o CPF possui 11 dígitos ou 10 dígitos com 'X' no final
    if len(cpf_cliente) == 11 or (len(cpf_cliente) == 10 and cpf_cliente[-1] == 'X'):
        # Verificar se o CPF já existe no arquivo
        with open("cadastro_cliente.txt", "r") as arquivo:
            for linha in arquivo:
                if cpf_cliente in linha:
                    print("CPF já cadastrado.")
                    return None
        return cpf_cliente
    else:
        print("CPF inválido.")
        return None
    
# Função para validar a data de nascimento do cliente
def validar_nasc(data_nasc):
    # Remover todos os caracteres que não são dígitos ou barras "/"
    data_nasc = re.sub(r'^[0-9/]$', '', data_nasc)
    
    # Verificar se a data de nascimento tem o formato correto (dd/mm/aaaa)
    if len(data_nasc) != 10 or data_nasc[2] != '/' or data_nasc[5] != '/':
        return False
    
    # Separar o dia, mês e ano
    dia, mes, ano = map(int, data_nasc.split('/'))
    
    # Verificar se o ano está entre 1899 e 2006
    if not 1899 <= ano <= 2006:
        return False
    
    # Verificar se o mês está entre 1 e 12
    if not 1 <= mes <= 12:
        return False
    
    # Verificar se o dia é válido para o mês especificado
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 1 <= dia <= 31
    elif mes in [4, 6, 9, 11]:
        return 1 <= dia <= 30
    elif mes == 2:
        # Verificar se é ano bissexto para ajustar os dias de fevereiro
        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
            return 1 <= dia <= 29
        else:
            return 1 <= dia <= 28
    else:
        return False

# Função para validar informações adicionais 
def validar_info(outras_infos):
    return len(outras_infos) <= 30

# Função para adicionar informações ao arquivo
def adicionar_informacoes_arquivo(nome_arquivo, id_cliente, nome_cliente, cpf_cliente, data_nasc, infos_adc):
    with open(nome_arquivo, 'a') as arquivo:
        id_formatado = id_cliente.zfill(10)
        nome_formatado = nome_cliente.ljust(40) 
        data_formatada = data_nasc.replace('/', '')
        informacoes = f"{id_formatado}{nome_formatado}{cpf_cliente}{data_formatada}{infos_adc}"
        arquivo.write(f'{informacoes}\n')

# Função para verificar se o arquivo existe e escrever o cabeçalho se necessário
def verificar_arquivo(nome_arquivo):
    if not os.path.isfile(nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write("CADASTRO CLIENTE\n")

# Função para cadastrar o ID do cliente
def proximo_id():
    # Abre o arquivo para leitura
    with open("cadastro_cliente.txt", "r") as arquivo:
        # Lê todas as linhas do arquivo
        linhas = arquivo.readlines()
        # Se o arquivo estiver vazio, retorna o primeiro ID possível
        if len(linhas) <= 1:
            return '0000000001'
        # Caso contrário, obtém o último ID registrado
        ultimo_id = linhas[-1].split()[0]
        # Extrai apenas os dígitos do último ID
        ultimo_id_digitos = ''.join(filter(str.isdigit, ultimo_id))
        # Incrementa o último ID em 1
        proximo = int(ultimo_id_digitos) + 1
        # Retorna o próximo ID preenchido com zeros à esquerda
        return str(proximo).zfill(10)

def cadastro_id():
    return proximo_id()
   
# Função para cadastrar o cliente
def cadastro_cliente():
    while True:
        nome_cliente = input("Insira o nome do cliente (máximo de 40 caracteres e sem espaços): ").upper()
        if validar_nome(nome_cliente):
            return nome_cliente
        else:
            print("Nome inválido. Por favor, insira um nome com no máximo 40 caracteres.")

# Função para cadastrar o CPF do cliente
def cadastro_cpf():
    while True:
        cpf_cliente = input("Digite o CPF do cliente: ").replace('.', '').replace('-', '')
        cpf_validado = validar_cpf(cpf_cliente)
        if cpf_validado:
            return cpf_validado


# Função para cadastrar a data de nascimento do cliente
def cadastro_nasc():
    while True:  
        data_nasc = input("Digite sua data de nascimento (no formato dd/mm/aaaa): ").replace(' ', '')
        if validar_nasc(data_nasc):
            return data_nasc
        else:
            print("Data de nascimento inválida, insira no formato dd/mm/aaaa")

# Função para cadastrar informações adicionais do cliente
def outras_infos():
    while True:
        infos_adc = input("Digite as informações adicionais do cliente ").replace(' ', '')
        if validar_info(infos_adc):
            return infos_adc
        else:
            print("Limite de caracteres excedidos. Máx 30 ")

# Função principal para o cadastro_cliente completo
def cadastrar_cliente():
    verificar_arquivo("cadastro_cliente.txt")  
    id_cliente = cadastro_id()
    nome_cliente = cadastro_cliente()
    cpf_cliente = cadastro_cpf()
    data_nasc = cadastro_nasc()
    infos_adc = outras_infos()
    adicionar_informacoes_arquivo("cadastro_cliente.txt", id_cliente, nome_cliente, cpf_cliente, data_nasc, infos_adc)
    print(f"Cliente cadastrado: ID: {id_cliente}, Nome: {nome_cliente}, CPF: {cpf_cliente}, Data de nascimento: {data_nasc}, Inf. Adicionais: {infos_adc}")

# Chamada da função para cadastrar um cliente
cadastrar_cliente()
