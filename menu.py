class GerenciadorCadastros:
    """
    Classe responsável por gerenciar os cadastros de clientes, produtos, pedidos e itens do pedido.
    """

    @staticmethod
    def cadastrar_cliente():
        """
        Realiza o cadastro de um cliente.
        """
        try:
            from cadastros.cadastro_cliente import cadastro_cliente_txt

            cadastro_cliente_txt()
        except ImportError:
            print("Erro ao importar o módulo cadastro_cliente.")

    @staticmethod
    def cadastrar_produto():
        """
        Realiza o cadastro de um produto.
        """
        try:
            from cadastros.cadastro_produto import cadastro_produto_txt

            cadastro_produto_txt()
        except ImportError:
            print("Erro ao importar o módulo cadastro_produto.")

    @staticmethod
    def cadastrar_pedido():
        """
        Realiza o cadastro de um pedido.
        """
        try:
            from cadastros.cadastro_pedido import cadastro_pedido_txt

            cadastro_pedido_txt()
        except ImportError:
            print("Erro ao importar o módulo cadastro_pedido.")

    @staticmethod
    def cadastrar_itens_pedido():
        """
        Realiza o cadastro de itens do pedido.
        """
        try:
            from cadastros.cadastro_itens_pedido import cadastro_itens_txt

            cadastro_itens_txt()
        except ImportError:
            print("Erro ao importar o módulo cadastro_itens_pedido.")

    @staticmethod
    def remover_cliente(id_cliente):
        """
        Remove um cliente pelo ID.
        """
        id_cliente = id_cliente.rjust(10, "0")
        try:
            with open("arquivos_cadastro/cadastro_cliente.txt", "r+") as arquivo:
                linhas = arquivo.readlines()
                encontrado = False
                arquivo.seek(0)
                for linha in linhas:
                    if linha.startswith(id_cliente):
                        encontrado = True
                        continue
                    arquivo.write(linha)
                arquivo.truncate()

            if encontrado:
                print("Cliente removido com sucesso.")
            else:
                print("Cliente com ID", id_cliente, "não encontrado.")
                return Cliente.escolhas_cliente()

        except FileNotFoundError:
            print("Arquivo 'cadastro_cliente.txt' não encontrado.")
        except Exception as e:
            print(f"Erro ao remover cliente: {str(e)}")

    @staticmethod
    def remover_produto(id_produto):
        """
        Remove um produto pelo ID.
        """
        try:
            with open("arquivos_cadastro/cadastro_produto.txt", "r+") as arquivo:
                linhas = arquivo.readlines()
                encontrado = False
                arquivo.seek(0)
                for linha in linhas:
                    if linha.startswith(id_produto):
                        encontrado = True
                        continue
                    arquivo.write(linha)
                arquivo.truncate()

            if encontrado:
                print(f"Produto com ID {id_produto} removido com sucesso.")
            else:
                print(f"Produto com ID {id_produto} não encontrado.")
                return Produto.escolhas_produto()

        except FileNotFoundError:
            print("Arquivo 'cadastro_produto.txt' não encontrado.")
        except Exception as e:
            print(f"Erro ao remover produto: {str(e)}")

    @staticmethod
    def verificar_arquivo(nome_arquivo):
        """
        Verifica a existência de um arquivo.
        """
        try:
            from cadastros.cadastro_itens_pedido import verificar_arquivo

            verificar_arquivo(nome_arquivo)
        except FileNotFoundError:
            print(f"Arquivo {nome_arquivo} não encontrado.")
        except Exception as e:
            print(f"Erro ao verificar arquivo: {e}")


class Cliente:
    """
    Classe responsável por operações relacionadas a clientes.
    """

    @staticmethod
    def cadastrar_cliente_txt():
        """
        Método estático para cadastrar um cliente e exibir opções após o cadastro.
        """
        GerenciadorCadastros.cadastrar_cliente()
        Cliente.escolhas_cliente()

    @staticmethod
    def remover_cliente_menu():
        """
        Método estático para solicitar o ID do cliente a ser removido.
        """

        with open("arquivos_cadastro/cadastro_cliente.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) < 2 or linhas[1].strip() == "":
                print("Nenhum cliente cadastrado")
                return Cliente.escolhas_cliente()

        id_cliente = input("Digite o ID do cliente a ser removido: ")
        GerenciadorCadastros.remover_cliente(id_cliente)

    @staticmethod
    def escolhas_cliente():
        """
        Método estático para exibir opções relacionadas a clientes após o cadastro.
        """
        opcoes = [
            "Cadastrar outro cliente",
            "Remover cliente",
            "Alterar cliente",
            "Consultar clientes",
            "Voltar ao Menu",
            "Sair",
        ]
        acoes = {
            "Cadastrar outro cliente": Cliente.cadastrar_cliente_txt,
            "Remover cliente": Cliente.remover_cliente_menu,
            "Alterar cliente": Cliente.alterar_cliente_menu,
            "Consultar clientes": Cliente.consultar_clientes,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)

    @staticmethod
    def consultar_clientes():
        """
        Método estático para consultar e exibir clientes.
        """
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
            Cliente.escolhas_cliente()
        else:
            print("Não há clientes cadastrados.")
            Cliente.escolhas_cliente()

    @staticmethod
    def alterar_cliente(id_cliente):
        """
        Método estático para alterar informações de um cliente.
        """
        id_cliente = id_cliente.zfill(10)

        try:
            encontrado = False
            clientes_atualizados = []
            with open("arquivos_cadastro/cadastro_cliente.txt", "r") as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    if linha.startswith(id_cliente):
                        encontrado = True
                        novo_nome = input(
                            "Digite o novo nome do cliente (máximo 40 caracteres): "
                        )
                        novo_cpf = input(
                            "Digite o novo CPF do cliente (11 caracteres, aceita X): "
                        )
                        nova_data_nascimento = input(
                            "Digite a nova data de nascimento do cliente (DD/MM/AAAA - somente números): "
                        )
                        info_adicionais = input(
                            "Digite as novas informações adicionais do cliente (máximo 30 caracteres): "
                        )

                        if len(novo_nome) > 40:
                            print(
                                "Erro: Nome excede o limite de 40 caracteres. Alteração não realizada."
                            )
                            return Cliente.escolhas_cliente

                        if (
                            len(novo_cpf) != 11
                            or not novo_cpf[:-1].isdigit()
                            or (novo_cpf[-1] not in "0123456789X")
                        ):
                            print(
                                "Erro: CPF inválido. Deve ter 11 caracteres numéricos, aceitando X no último."
                            )
                            return Cliente.escolhas_cliente

                        if (
                            len(nova_data_nascimento) != 10
                            or not nova_data_nascimento.replace("/", "").isdigit()
                        ):
                            print(
                                "Erro: Data de nascimento inválida. Formato esperado: DD/MM/AAAA."
                            )
                            return Cliente.escolhas_cliente

                        if len(info_adicionais) > 30:
                            print(
                                "Erro: Informações adicionais excedem o limite de 30 caracteres. Alteração não realizada."
                            )
                            return Cliente.escolhas_cliente

                        nova_data_nascimento = nova_data_nascimento.replace("/", "")

                        linha = (
                            id_cliente.ljust(10)
                            + novo_nome.ljust(40)
                            + novo_cpf.ljust(11)
                            + nova_data_nascimento.ljust(8)
                            + info_adicionais[:30].ljust(30)
                            + "\n"
                        )
                    clientes_atualizados.append(linha)
                    print("sucesso")

            if not encontrado:
                print(f"ID do cliente {id_cliente} não encontrado.")
                return Cliente.escolhas_cliente()

            with open("arquivos_cadastro/cadastro_cliente.txt", "w") as arquivo:
                arquivo.writelines(clientes_atualizados)

        except FileNotFoundError:
            print("Arquivo 'cadastro_cliente.txt' não encontrado.")
        except Exception as e:
            print(f"Erro ao alterar cliente: {str(e)}")

    @staticmethod
    def alterar_cliente_menu():
        """
        Método estático para solicitar o ID do cliente e chamar a função de alteração de cliente.
        """
        with open("arquivos_cadastro/cadastro_cliente.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) < 2 or linhas[1].strip() == "":
                print("Nenhum cliente cadastrado")
                return Cliente.escolhas_cliente()

        id_cliente = input("Digite o ID do cliente a ser alterado: ")
        Cliente.alterar_cliente(id_cliente)

    @staticmethod
    def alterar_produto(id_produto, novo_nome, nova_quantidade, novo_preco):
        """
        Altera um produto pelo ID.
        """
        try:
            encontrado = False
            produtos_atualizados = []
            with open("arquivos_cadastro/cadastro_produto.txt", "r") as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    if linha.startswith(id_produto):
                        encontrado = True
                        linha = f"{id_produto}{novo_nome.ljust(30)}{str(nova_quantidade).rjust(5)}{str(novo_preco).rjust(15)}\n"
                    produtos_atualizados.append(linha)

            if not encontrado:
                print(f"Produto com ID {id_produto} não encontrado.")
                return Produto.escolhas_produto()

            with open("arquivos_cadastro/cadastro_produto.txt", "w") as arquivo:
                arquivo.writelines(produtos_atualizados)

            print("Produto alterado com sucesso.")

        except FileNotFoundError:
            print("Arquivo 'cadastro_produto.txt' não encontrado.")
        except Exception as e:
            print(f"Erro ao alterar produto: {str(e)}")


class Consultas:
    """
    Classe responsável por realizar consultas nos arquivos de cadastro.
    """

    @staticmethod
    def formatar_cliente(linha):
        """
        Formata os dados de um cliente.
        """
        id_cliente = linha[:10].strip()
        nome = linha[10:40].strip()
        cpf = linha[50:61].strip()

        if (cpf.isdigit() and len(cpf) == 11) or (
            cpf[:-1].isdigit() and cpf[-1] == "X" and len(cpf) == 11
        ):
            cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            return {"id": id_cliente, "nome": nome, "cpf": cpf_formatado}
        else:
            print(f"Erro na formatação do CPF do cliente {id_cliente}. Ignorando.")
            return None

    @staticmethod
    def formatar_produto(linha):
        """
        Formata os dados de um produto.
        """
        id_produto = linha[:10].strip()
        nome = linha[10:40].strip()
        quantidade = int(linha[58:63].strip())
        preco_str = linha[70:].strip()
        if preco_str and not preco_str.replace(",", "").isdigit():
            print(f"Erro: Preço inválido encontrado na linha: {linha}")
            return None
        else:
            preco = float(preco_str.replace(",", "."))
            return {
                "id": id_produto,
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco,
            }

    @staticmethod
    def formatar_pedido(linha):
        """
        Formata os dados de um pedido.
        """
        id_pedido = linha[:10].strip()
        id_cliente = linha[10:20].strip()
        data_pedido = linha[20:28].strip()
        pedido_status = linha[28:38].strip()
        valor_total = linha[38:].strip()
        return {
            "id_pedido": id_pedido,
            "id_cliente": id_cliente,
            "data_pedido": data_pedido,
            "pedido_status": pedido_status,
            "valor_total": valor_total,
        }

    @staticmethod
    def consultar_arquivo(caminho_arquivo, formatar_funcao):
        """
        Consulta um arquivo de cadastro e formata os registros de acordo com a função especificada.
        """
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
        """
        Calcula o valor total de um pedido com base nos itens associados a ele.
        """
        total = 0
        try:
            with open("arquivos_cadastro/cadastro_itens_pedido.txt", "r") as arquivo:
                next(arquivo)
                for linha in arquivo:
                    id_pedido_linha = linha[:10].strip()
                    if id_pedido == id_pedido_linha:
                        print("ID do Pedido encontrado:", id_pedido)
                        quantidade = int(linha[40:50].strip())
                        preco_str = linha[50:].strip()
                        if preco_str:
                            preco = float(preco_str.replace(",", "."))
                            print("Quantidade:", quantidade)
                            print("Preço:", preco)
                            total += preco * quantidade
                        else:
                            print("Preço não encontrado na linha:", linha)
        except Exception as e:
            print(f"Erro ao calcular valor total do pedido: {str(e)}")
            return 0

        return total


class Produto:
    """
    Classe responsável por operações relacionadas a produtos.
    """

    @staticmethod
    def cadastrar_produto_txt():
        """
        Método estático para cadastrar um produto e exibir opções após o cadastro.
        """
        GerenciadorCadastros.cadastrar_produto()
        Produto.escolhas_produto()

    @staticmethod
    def remover_produto_menu():
        """
        Método estático para solicitar o ID do produto a ser removido.
        """
        with open("arquivos_cadastro/cadastro_produto.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) < 2 or linhas[1].strip() == "":
                print("Nenhum produto cadastrado")
                return Produto.escolhas_produto()

        id_produto = input("Digite o ID do produto a ser removido: ")

        id_produto = id_produto.zfill(10)
        GerenciadorCadastros.remover_produto(id_produto)

    @staticmethod
    def escolhas_produto():
        """
        Método estático para exibir opções relacionadas a produtos após o cadastro.
        """
        opcoes = [
            "Cadastrar outro produto",
            "Remover produto",
            "Alterar produto",
            "Consultar produtos",
            "Voltar ao Menu",
            "Sair",
        ]
        acoes = {
            "Cadastrar outro produto": Produto.cadastrar_produto_txt,
            "Remover produto": Produto.remover_produto_menu,
            "Alterar produto": Produto.alterar_produto_menu,
            "Consultar produtos": Produto.consultar_produtos,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)

    @staticmethod
    def consultar_produtos():
        """
        Método estático para consultar e exibir produtos.
        """
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
                    f"ID: {produto['id']}, Nome: {produto['nome']}, Quantidade: {produto['quantidade']}, Preço: {produto['preco']}"
                )
            Produto.escolhas_produto()
        else:
            print("Não há produtos cadastrados.")
            Produto.escolhas_produto()

    @staticmethod
    def alterar_produto_menu():
        """
        Método estático para solicitar o ID do produto e chamar a função de alteração de produto.
        """
        with open("arquivos_cadastro/cadastro_produto.txt", "r+") as arquivo:
            linhas = arquivo.readlines()
            if len(linhas) < 2 or linhas[1].strip() == "":
                print("Nenhum produto cadastrado")
                return Produto.escolhas_produto()

        id_produto = input("Digite o ID do produto a ser alterado: ")
        novo_nome = input("Digite o novo nome do produto: ")
        nova_quantidade = int(input("Digite a nova quantidade do produto: "))
        novo_preco = float(input("Digite o novo preço do produto: "))

        GerenciadorCadastros.alterar_produto(
            id_produto, novo_nome, nova_quantidade, novo_preco
        )


class SistemaERP:
    """
    Classe responsável por operações relacionadas ao sistema ERP.
    """

    @staticmethod
    def menu_principal():
        """
        Método estático para exibir o menu principal do sistema.
        """
        opcoes = ["Clientes", "Produtos", "Pedidos", "Sair"]
        acoes = {
            "Clientes": Cliente.escolhas_cliente,
            "Produtos": Produto.escolhas_produto,
            "Pedidos": Pedido.escolhas_pedido,
            "Sair": exit,
        }
        SistemaERP.menu_escolha(
            "Bem-vindo ao Sistema ERP. O que deseja fazer?", opcoes, acoes
        )

    @staticmethod
    def menu_escolha(mensagem, opcoes, acoes):
        """
        Método estático para exibir um menu de escolhas.
        """
        print("\n" + mensagem)
        for i, opcao in enumerate(opcoes, 1):
            print(f"{i}. {opcao}")
        escolha = input("Digite o número correspondente à sua escolha: ")
        try:
            escolha_numero = int(escolha)
            if 1 <= escolha_numero <= len(opcoes):
                opcao_escolhida = opcoes[escolha_numero - 1]
                acao = acoes[opcao_escolhida]
                acao()
            else:
                print(
                    "Escolha inválida. Por favor, digite um número correspondente à sua escolha."
                )
        except ValueError:
            print(
                "Escolha inválida. Por favor, digite um número correspondente à sua escolha."
            )

    @staticmethod
    def cabecalho():
        """
        Método estático para exibir o cabeçalho do sistema.
        """
        print("\n" + "-" * 30)
        print("SISTEMA ERP")
        print("-" * 30)
        SistemaERP.menu_principal()


class Pedido:
    """
    Classe responsável por operações relacionadas a pedidos.
    """

    @staticmethod
    def escolhas_pedido():
        """
        Método estático para exibir opções relacionadas a pedidos.
        """
        opcoes = ["Cadastrar pedido", "Consultar pedidos", "Voltar ao Menu", "Sair"]
        acoes = {
            "Cadastrar pedido": Pedido.cadastrar_pedido,
            "Consultar pedidos": Pedido.consultar_pedidos,
            "Voltar ao Menu": SistemaERP.cabecalho,
            "Sair": exit,
        }
        SistemaERP.menu_escolha("O que deseja fazer?", opcoes, acoes)

    @staticmethod
    def cadastrar_pedido():
        """
        Método estático para cadastrar um pedido.
        """
        GerenciadorCadastros.cadastrar_pedido()
        Pedido.escolhas_pedido()

    @staticmethod
    def consultar_pedidos():
        """
        Método estático para consultar pedidos.
        """
        print("-" * 30)
        print("Você está no menu de consulta de pedidos")
        print("-" * 30)

        pedidos = Consultas.consultar_arquivo(
            "arquivos_cadastro/cadastro_pedido.txt", Consultas.formatar_pedido
        )
        if pedidos:
            print("Pedidos Cadastrados:")
            for pedido in pedidos:
                valor_total = Consultas.calcular_valor_total_pedido(pedido["id_pedido"])
                print(
                    f"ID Pedido: {pedido['id_pedido']}, ID Cliente: {pedido['id_cliente']}, Data: {pedido['data_pedido']}, Status: {pedido['pedido_status']}, Valor Total: {valor_total}"
                )
            Pedido.escolhas_pedido()
        else:
            print("Não há pedidos cadastrados.")
            Pedido.escolhas_pedido()


SistemaERP.cabecalho()
