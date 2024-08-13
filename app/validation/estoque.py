from ..exceptions.estoque import ProdutoException


class EstoqueValidacao:

    @staticmethod
    def validar_estoque(estoque):
        if estoque < 0:
            raise ProdutoException("Quantidade em estoque inválida")

    @staticmethod
    def validar_preco(preco):
        if preco < 0:
            raise ProdutoException("Preço inválido")

    @staticmethod
    def validar_nome_produto(nome_produto):
        if not nome_produto:
            raise ProdutoException("Nome do produto não pode ser vazio")
