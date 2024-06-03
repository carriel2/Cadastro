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
