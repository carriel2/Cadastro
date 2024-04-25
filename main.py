from datetime import datetime

class GerenciadorCadastros:

    @staticmethod
    def cadastrar_cliente():
        from cadastros.cadastro_cliente import cadastro_cliente_txt
        cadastro_cliente_txt()

    @staticmethod
    def cadastrar_produto():
        from cadastros.cadastro_produto import cadastro_produto_txt
        cadastro_produto_txt()

    @staticmethod
    def cadastrar_pedido():
        from cadastros.cadastro_pedido import cadastro_pedido_txt
        cadastro_pedido_txt()

    @staticmethod
    def cadastrar_itens_pedido():
        from cadastros.cadastro_itens_pedido import cadastro_itens_txt
        cadastro_itens_txt()

    @staticmethod
    def verificar_arquivo(nome_arquivo):
        from cadastros.cadastro_itens_pedido import verificar_arquivo
        verificar_arquivo(nome_arquivo)


class Consultas:

    @staticmethod
    def formatar_cliente(linha):
        id_cliente = linha[:10].strip()
        nome = linha[10:40].strip()
        cpf = linha[50:61].strip()
        
        # Verificar se o CPF possui 11 dígitos ou 10 dígitos + "X" no final
        if (cpf.isdigit() and len(cpf) == 11) or (cpf[:-1].isdigit() and cpf[-1] == "X" and len(cpf) == 11):
            # Se o CPF tiver 11 dígitos ou 10 dígitos + "X", formatá-lo
            cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            return {"id": id_cliente, "nome": nome, "cpf": cpf_formatado}
        else:
            print(f"Erro na formatação do CPF do cliente {id_cliente}. Ignorando.")
            return None


    @staticmethod
    def formatar_produto(linha):
        id_produto = linha[:10].strip()
        nome = linha[10:40].strip()
        quantidade = int(linha[58:63].strip())
        preco = float(linha[64:].strip())
        return {
            "id": id_produto,
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco,
        }

    @staticmethod
    def formatar_pedido(linha):
        id_pedido = linha[:10].strip()
        id_cliente = linha[10:20].strip()
        data_pedido = linha[20:28].strip()
        pedido_status = linha[28:38].strip()  # Ajuste no tamanho do campo do status do pedido
        valor_total = linha[38:].strip()  # Ajuste na posição do valor total
        return {
            "id_pedido": id_pedido,
            "id_cliente": id_cliente,
            "data_pedido": data_pedido,
            "pedido_status": pedido_status,
            "valor_total": valor_total,
        }


    @staticmethod
    def consultar_arquivo(caminho_arquivo, formatar_funcao):
        try:
            with open(caminho_arquivo, "r") as arquivo:
                registros = []
                next(arquivo)
                for linha in arquivo:
                    registro_formatado = formatar_funcao(linha)
                    if registro_formatado:
                        registros.append(registro_formatado)
                return registros
        except FileNotFoundError:
            print(f"Arquivo {caminho_arquivo} não encontrado.")
            return []

    @staticmethod
    def calcular_valor_total_pedido(id_pedido):
        total = 0
        try:
            with open("arquivos_cadastro/cadastro_itens_pedido.txt", "r") as arquivo:
                next(arquivo)  # Ignorar cabeçalho
                for linha in arquivo:
                    id_pedido_linha = linha[:10].strip()
                    if id_pedido == id_pedido_linha:
                        print("ID do Pedido encontrado:", id_pedido)
                        quantidade = int(linha[40:50].strip())
                        preco_str = linha[50:].strip()
                        if preco_str:
                            preco = float(preco_str)
                            print("Quantidade:", quantidade)
                            print("Preço:", preco)
                            total += preco * quantidade
                        else:
                            print("Preço não encontrado na linha:", linha)
        except Exception as e:
            print(f"Erro ao calcular valor total do pedido: {str(e)}")
            return 0  # Retorna 0 em caso de erro

        return total


class Cliente:

    @staticmethod
    def cadastrar_cliente_txt():
        GerenciadorCadastros.cadastrar_cliente()
        Cliente.escolhas_cliente()

    @staticmethod
    def escolhas_cliente():
        opcoes = ["Cadastrar outro cliente", "Voltar ao Menu", "Sair"]
        acoes = {
            "Cadastrar outro cliente": Cliente.cadastrar_cliente_txt,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)

    @staticmethod
    def consultar_clientes():
        print("-" * 30)
        print("Você está no menu de consulta de clientes")
        print("-" * 30)

        clientes = Consultas.consultar_arquivo(
            "arquivos_cadastro/cadastro_cliente.txt", Consultas.formatar_cliente
        )
        if clientes:
            print("Clientes Cadastrados:")
            for cliente in clientes:
                print(
                    f"ID: {cliente['id']}, Nome: {cliente['nome']}, CPF: {cliente['cpf']}"
                )
            Cliente.escolhas_cliente()  # Após consultar, oferecer opções novamente
        else:
            print("Nenhum cliente cadastrado.")
            Cliente.escolhas_cliente()  # Após consultar, oferecer opções novamente


class Produto:

    @staticmethod
    def cadastrar_produto_txt():
        GerenciadorCadastros.cadastrar_produto()
        Produto.escolhas_produto()

    @staticmethod
    def escolhas_produto():
        opcoes = ["Cadastrar outro produto", "Voltar ao Menu", "Consultar Produtos", "Sair"]
        acoes = {
            "Cadastrar outro produto": Produto.cadastrar_produto_txt,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Consultar Produtos": Produto.consultar_produtos,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)

    @staticmethod
    def consultar_produtos():
        print("-" * 30)
        print("Você está no menu de consulta de produtos")
        print("-" * 30)

        produtos = Consultas.consultar_arquivo(
            "arquivos_cadastro/cadastro_produto.txt", Consultas.formatar_produto
        )
        if produtos:
            print("Produtos Cadastrados:")
            for produto in produtos:
                print(
                    f"ID: {produto['id']}, Nome: {produto['nome']}, Quantidade em Estoque: {produto['quantidade']}, Preço Unitário: R$ {produto['preco']}"
                )
            Produto.escolhas_produto()  # Após consultar, oferecer opções novamente
        else:
            print("Nenhum produto cadastrado.")
            Produto.escolhas_produto()  # Após consultar, oferecer opções novamente


class Pedido:

    @staticmethod
    def cadastrar_pedido_txt():
        GerenciadorCadastros.cadastrar_pedido()
        Pedido.escolhas_pedido()

    @staticmethod
    def escolhas_pedido():
        opcoes = ["Cadastrar outro pedido", "Voltar ao Menu", "Consultar Pedidos", "Sair"]
        acoes = {
            "Cadastrar outro pedido": Pedido.cadastrar_pedido_txt,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Consultar Pedidos": Pedido.consultar_pedidos,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)


    @staticmethod
    def calcular_valor_total_pedido(id_pedido):
        total = 0
        try:
            with open("arquivos_cadastro/cadastro_itens_pedido.txt", "r") as arquivo:
                next(arquivo)  
                for linha in arquivo:
                    id_pedido_linha = linha[0:10].strip()  
                    if id_pedido == id_pedido_linha:
                        quantidade_str = linha[20:30].strip()
                        try:
                            quantidade = int(quantidade_str)
                            preco_str = linha[30:].strip()
                            try:
                                preco = float(preco_str)
                                total += preco * quantidade
                            except ValueError:
                                print("Erro: Valor do preço não pôde ser convertido para float:", preco_str)
                        except ValueError:
                            print("Erro: Valor da quantidade não pôde ser convertido para int:", quantidade_str)
        except FileNotFoundError:
            print("Arquivo 'cadastro_itens_pedido.txt' não encontrado.")
        except Exception as e:
            print(f"Erro ao calcular valor total do pedido: {str(e)}")
            return 0  
        return total

    @staticmethod
    def consultar_pedidos():
        print("-" * 30)
        print("Você está no menu de consulta de pedidos")
        print("-" * 30)

        pedidos = Consultas.consultar_arquivo(
            "arquivos_cadastro/cadastro_pedido.txt", Consultas.formatar_pedido
        )
        if pedidos:
            print("Pedidos Cadastrados:")
            for pedido in pedidos:
                # Formatando a data do pedido
                data_formatada = datetime.strptime(pedido['data_pedido'], '%d%m%Y').strftime('%d/%m/%Y')
                valor_total = Pedido.calcular_valor_total_pedido(pedido["id_pedido"])
                print(
                    f"ID Pedido: {pedido['id_pedido']}, ID Cliente: {pedido['id_cliente']}, Data do Pedido: {data_formatada}, Status do Pedido: {pedido['pedido_status']}, Valor Total: R$ {valor_total}"
                )
            Pedido.escolhas_pedido()  # Após consultar, oferecer opções novamente
        else:
            print("Nenhum pedido cadastrado.")
            Pedido.escolhas_pedido()  # Após consultar, oferecer opções novamente


class ItensPedido:

    @staticmethod
    def cadastrar_itens_txt():
        GerenciadorCadastros.cadastrar_itens_pedido()
        ItensPedido.escolhas_itens()

    @staticmethod
    def escolhas_itens():
        opcoes = ["Cadastrar outro item", "Voltar ao Menu", "Sair"]
        acoes = {
            "Cadastrar outro item": ItensPedido.cadastrar_itens_txt,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)


class SistemaERP:

    @staticmethod
    def menu_escolha(pergunta, opcoes, acoes):
        while True:
            print(pergunta)
            for opcao in opcoes:
                print(f"{opcoes.index(opcao) + 1}. {opcao}")
            escolha = input("Escolha uma opção: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
                acao_escolhida = acoes[opcoes[int(escolha) - 1]]
                acao_escolhida()
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

    @staticmethod
    def cabecalho():
        largura = 30
        texto = "Bem Vindo a PedralhaERP"
        text_center = texto.center(largura)

        print("-" * 30)
        print(text_center)
        print("-" * 30)

        largura = 30
        menu = "MENU"
        texto = " 1 - Cadastrar Cliente \n 2 - Cadastrar Produto \n 3 - Cadastrar Pedido \n 4 - Cadastrar itens no Pedido \n 5 - Consultar Clientes \n 6 - Consultar Produtos \n 7 - Consultar Pedidos \n 8 - Sair"
        text_center = menu.center(largura)

        print("-" * 30)
        print(text_center)
        print("-" * 30)
        print(texto)

        escolha = input("Escolha uma das opções do menu: ")

        if escolha == "8":
            print("Obrigado pela preferência. Volte sempre!")
            exit()
        else:
            SistemaERP.direcionar_menu(escolha)

    @staticmethod
    def direcionar_menu(escolha):
        opcoes_menu = {
            "1": SistemaERP.menu_cliente,
            "2": SistemaERP.menu_produto,
            "3": SistemaERP.menu_pedido,
            "4": SistemaERP.menu_itens_pedido,
            "5": SistemaERP.menu_consultar_clientes,
            "6": SistemaERP.menu_consultar_produtos,
            "7": SistemaERP.menu_consultar_pedidos,
            "8": "Sair",
        }

        funcao_menu = opcoes_menu.get(escolha)

        if funcao_menu:
            funcao_menu()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            SistemaERP.cabecalho()

    @staticmethod
    def menu_cliente():
        print("-" * 30)
        print("Você está no menu de cadastro de clientes")
        print("-" * 30)

        Cliente.cadastrar_cliente_txt()

    @staticmethod
    def menu_produto():
        print("-" * 30)
        print("Você está no menu de cadastro de produtos")
        print("-" * 30)

        Produto.cadastrar_produto_txt()

    @staticmethod
    def menu_pedido():
        print("-" * 30)
        print("Você está no menu de cadastro de pedidos")
        print("-" * 30)

        Pedido.cadastrar_pedido_txt()

    @staticmethod
    def menu_itens_pedido():
        print("-" * 30)
        print("Você está no menu de cadastro de itens do pedido")
        print("-" * 30)

        ItensPedido.cadastrar_itens_txt()

    @staticmethod
    def menu_consultar_clientes():
        print("-" * 30)
        print("Você está no menu de consulta de clientes")
        print("-" * 30)

        Cliente.consultar_clientes()

    @staticmethod
    def menu_consultar_produtos():
        print("-" * 30)
        print("Você está no menu de consulta de produtos")
        print("-" * 30)

        Produto.consultar_produtos()

    @staticmethod
    def menu_consultar_pedidos():
        print("-" * 30)
        print("Você está no menu de consulta de pedidos")
        print("-" * 30)

        Pedido.consultar_pedidos()


gerenciador = GerenciadorCadastros()
sistema = SistemaERP()
sistema.cabecalho()
