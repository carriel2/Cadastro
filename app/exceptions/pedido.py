class PedidoException(Exception):
    """
    Classe pai para excecoes do Pedido
    """


class PedidoNaoEncontrado(PedidoException):
    """
    Excecao para quando o Pedido não for encontrado no banco de dados durante o SELECT
    """
