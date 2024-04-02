import os.path
import re

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
            arquivo.write("CADASTRO CLIENTE\n")

def adicionar_informacoes_arquivo(nome_arquivo, id_cliente, nome_cliente, cpf_cliente, data_nasc, infos_adc):
    """
    Adiciona as informações ao arquivo.
    """
    with open(nome_arquivo, 'a') as arquivo:
        id_formatado = id_cliente.zfill(10)
        nome_formatado = nome_cliente.ljust(40) 
        data_formatada = data_nasc.replace('/', '')
        informacoes = f"{id_formatado}{nome_formatado}{cpf_cliente}{data_formatada}{infos_adc}"
        arquivo.write(f'{informacoes}\n')
        
def cadastro_cliente_txt():
    """
    Mostra no terminal que as informações foram cadastradas.
    Repassa para o arquivo de adicionar informações, o caminho e quais as variaveis que devem ser armazenadas
    na ordem correta. 
    """
    verificar_arquivo("cadastro_cliente.txt")
      
    id_cliente = cadastro_id()
    nome_cliente = cadastro_nome()
    cpf_cliente = cadastro_cpf()
    data_nasc = cadastro_nasc()
    infos_adc = cadastro_info()
    
    adicionar_informacoes_arquivo("arquivos_cadastro/cadastro_cliente.txt", id_cliente, nome_cliente, cpf_cliente, data_nasc, infos_adc)
    print(f"Cliente cadastrado: ID: {id_cliente}, Nome: {nome_cliente}, CPF: {cpf_cliente}, Data de nascimento: {data_nasc}, Inf. Adicionais: {infos_adc}")

def validar_nome(nome):
    """
    Valida o nome do cliente.
    """
    return bool(re.match("^[a-zA-Z]{1,40}$", nome))

def validar_cpf(cpf_cliente):
    """
    Valida o CPF do cliente e verifica se já existe no arquivo.
    """
    cpf_cliente = re.sub(r'[^0-9X]', '', cpf_cliente)
    
    if len(cpf_cliente) == 11 or (len(cpf_cliente) == 10 and cpf_cliente[-1] == 'X'):
        with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
            for linha in arquivo:
                if cpf_cliente in linha:
                    print("CPF já cadastrado.")
                    return None
        return cpf_cliente
    else:
        print("CPF inválido.")
        return None

def validar_nasc(data_nasc):
    """
    Valida a data de nascimento do cliente.
    """
    data_nasc = re.sub(r'^[0-9/]$', '', data_nasc)
    
    if len(data_nasc) != 10 or data_nasc[2] != '/' or data_nasc[5] != '/':
        return False
    
    dia, mes, ano = map(int, data_nasc.split('/'))
    
    if not 1899 <= ano <= 2006:
        return False
    
    if not 1 <= mes <= 12:
        return False
    
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 1 <= dia <= 31
    elif mes in [4, 6, 9, 11]:
        return 1 <= dia <= 30
    elif mes == 2:
        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
            return 1 <= dia <= 29
        else:
            return 1 <= dia <= 28
    else:
        return False

def validar_info(outras_infos):     
    """
    Valida as informações adicionais do cliente.
    """
    return len(outras_infos) <= 30

def proximo_id():
    """
    Obtém o próximo ID de cliente disponível.
    """
    with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        if len(linhas) <= 1:
            return '0000000001'
        
        ultimo_id = linhas[-1].split()[0]
        ultimo_id_digitos = ''.join(filter(str.isdigit, ultimo_id))
        proximo = int(ultimo_id_digitos) + 1
        return str(proximo).zfill(10)

def cadastro_id():
    """
    Realiza o cadastro do ID do cliente. POSIÇÃO 1-10
    """
    return proximo_id()

def cadastro_nome():
    """
    Realiza o cadastro do nome do cliente. POSIÇÃO 11-50
    """
    while True:
        nome_cliente = input("Insira o nome do cliente (máximo de 40 caracteres e sem espaços): ").upper()
        if validar_nome(nome_cliente):
            return nome_cliente
        else:
            print("Nome inválido. Por favor, insira um nome com no máximo 40 caracteres.")

def cadastro_cpf():
    """
    Realiza o cadastro do CPF do cliente. POSIÇÃO 51-62
    """
    while True:
        cpf_cliente = input("Digite o CPF do cliente: ").replace('.', '').replace('-', '')
        cpf_validado = validar_cpf(cpf_cliente)
        if cpf_validado:
            return cpf_validado

def cadastro_nasc():
    """
    Realiza o cadastro da data de nascimento do cliente. POSIÇÃO 62-70
    """
    while True:  
        data_nasc = input("Digite sua data de nascimento (no formato dd/mm/aaaa): ").replace(' ', '')
        if validar_nasc(data_nasc):
            return data_nasc
        else:
            print("Data de nascimento inválida, insira no formato dd/mm/aaaa")

def cadastro_info():
    """
    Realiza o cadastro das informações adicionais do cliente. POSIÇÃO 70-99
    """
    while True:
        infos_adc = input("Digite as informações adicionais do cliente ").replace(' ', '')
        if validar_info(infos_adc):
            return infos_adc
        else:
            print("Limite de caracteres excedidos. Máx 30 ")

