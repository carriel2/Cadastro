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
    def verificar_arquivo():
        from cadastros.cadastro_itens_pedido import verificar_arquivo
        verificar_arquivo()


class CadastroCliente:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def cadastrar_cliente_txt(self):
        
        gerenciador.cadastrar_cliente()
        
    

class CadastroProduto:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def cadastrar_produto_txt(self):
        print("Implemente a lógica para cadastrar produtos em um arquivo TXT aqui.")


class CadastroPedido:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def cadastrar_pedido_txt(self):
        print("Implemente a lógica para cadastrar pedidos em um arquivo TXT aqui.")


class CadastroItensPedido:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def cadastrar_itens_txt(self):
        print(
            "Implemente a lógica para cadastrar itens de pedido em um arquivo TXT aqui."
        )


class ConsultaClientes:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def consultar_clientes(self):
        print("Implemente a lógica para consultar clientes aqui.")


class ConsultaProdutos:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def consultar_produtos(self):
        print("Implemente a lógica para consultar produtos aqui.")


class ConsultaPedidos:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def consultar_pedidos(self):
        print("Implemente a lógica para consultar pedidos aqui.")


class SistemaERP:
    def __init__(self):
        self.cadastro_cliente = CadastroCliente("cadastro_cliente.txt")
        self.cadastro_produto = CadastroProduto("cadastro_produto.txt")
        self.cadastro_pedido = CadastroPedido("cadastro_pedido.txt")
        self.cadastro_itens_pedido = CadastroItensPedido("cadastro_itens_pedido.txt")
        self.consulta_clientes = ConsultaClientes("cadastro_cliente.txt")
        self.consulta_produtos = ConsultaProdutos("cadastro_produto.txt")
        self.consulta_pedidos = ConsultaPedidos("cadastro_pedido.txt")

    def cabecalho(self):
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
            self.direcionar_menu(escolha)

    def direcionar_menu(self, escolha):
        opcoes_menu = {
            "1": self.menu_cadastro_cliente,
            "2": self.menu_cadastro_produto,
            "3": self.menu_cadastro_pedido,
            "4": self.menu_cadastrar_itens_pedido,
            "5": self.menu_consultar_clientes,
            "6": self.menu_consultar_produtos,
            "7": self.menu_consultar_pedidos,
        }

        funcao_menu = opcoes_menu.get(escolha)

        if funcao_menu:
            funcao_menu()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            self.cabecalho()

    def menu_cadastro_cliente(self):
        print("-" * 30)
        print("Você está no menu de cadastro de clientes")
        print("-" * 30)

        self.cadastro_cliente.cadastrar_cliente_txt()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- CADASTRO CLIENTE / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
        )

        while escolha != "3":
            if escolha == "1":
                self.menu_cadastro_cliente()
            elif escolha == "2":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO CLIENTE / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
            )

        exit()

    def menu_cadastro_produto(self):
        print("-" * 30)
        print("Você está no menu de cadastro de produtos")
        print("-" * 30)

        self.cadastro_produto.cadastrar_produto_txt()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PRODUTO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
        )

        while escolha != "3":
            if escolha == "1":
                self.menu_cadastro_produto()
            elif escolha == "2":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PRODUTO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
            )

        exit()

    def menu_cadastro_pedido(self):
        print("-" * 30)
        print("Você está no menu de cadastro de pedidos")
        print("-" * 30)

        self.cadastro_pedido.cadastrar_pedido_txt()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
        )

        while escolha != "3":
            if escolha == "1":
                self.menu_cadastro_pedido()
            elif escolha == "2":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO PEDIDO / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
            )

        exit()

    def menu_cadastrar_itens_pedido(self):
        print("-" * 30)
        print("Você está no menu de cadastro de itens do pedido")
        print("-" * 30)

        self.cadastro_itens_pedido.cadastrar_itens_txt()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO ITEM / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
        )

        while escolha != "3":
            if escolha == "1":
                self.menu_cadastrar_itens_pedido()
            elif escolha == "2":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- CADASTRAR OUTRO ITEM / 2- RETORNAR PARA ESCOLHAS / 3- SAIR) "
            )

        exit()

    def menu_consultar_clientes(self):
        print("-" * 30)
        print("Você está no menu de consulta de clientes")
        print("-" * 30)

        self.consulta_clientes.consultar_clientes()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- RETORNAR PARA ESCOLHAS / 2- SAIR) "
        )

        while escolha != "2":
            if escolha == "1":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- RETORNAR PARA ESCOLHAS / 2- SAIR) "
            )

        exit()

    def menu_consultar_produtos(self):
        print("-" * 30)
        print("Você está no menu de consulta de produtos")
        print("-" * 30)

        self.consulta_produtos.consultar_produtos()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- RETORNAR PARA ESCOLHAS / 2- SAIR) "
        )

        while escolha != "2":
            if escolha == "1":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- RETORNAR PARA ESCOLHAS / 2- SAIR) "
            )

        exit()

    def menu_consultar_pedidos(self):
        print("-" * 30)
        print("Você está no menu de consulta de pedidos")
        print("-" * 30)

        self.consulta_pedidos.consultar_pedidos()

        escolha = input(
            "Digite o número da escolha desejada: \n (1- RETORNAR PARA ESCOLHAS / 2- SAIR) "
        )

        while escolha != "2":
            if escolha == "1":
                self.cabecalho()
            else:
                print("Insira uma escolha válida!")
            escolha = input(
                "Digite o número da escolha desejada: \n (1- RETORNAR PARA ESCOLHAS / 2- SAIR) "
            )

        exit()


gerenciador = GerenciadorCadastros()
sistema = SistemaERP()
sistema.cabecalho()


