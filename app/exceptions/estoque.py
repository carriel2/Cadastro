class ProdutoException(Exception):
    """
    Excecao pai para as excecoes de produto
    """


class ProdutoNaoEncontrado(ProdutoException):
    """
    Excecao para quando o produto nao for encontrado no txt
    """


class EstoqueInvalido(ProdutoException):
    """
    Excecao para quando o formato do estoque for inválido
    """


class EstoqueInsuficiente(ProdutoException):
    """
    Excecao para quando a quantidade do pedido for > que a quantidade em estoque
    """


class PrecoError(ProdutoException):
    """
    Excecao para quando o preco inserido for inválido
    """


class PrecoZeroError(ProdutoException):
    """
    Excecao para quando o preco inserido for < ou = a 0
    """


class NomeInvalido(ProdutoException):
    """
    Excecao para quando o nome inserida for invalida
    """


class ProdutoNaoEncontrado(ProdutoException):
    """
    Excecao para quando o produto nao for encontrado
    """

# --------------------------------------------------------------------------------------------- #
