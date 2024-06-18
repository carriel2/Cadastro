class DataException(Exception):
    """
    Exceção pai para exceções HTTP 400 de data
    """


class DataFuturaError(DataException):
    """
    Excecao para quando a data for maior que 3 dias no futuro
    """


class DataInvalida(DataException):
    """
    Excecao para quando for informado uma data invalida
    """


class DataNInvalida(DataException):
    """
    Excecao para quando a formatação da data estiver incorreta
    """


class AnoDataInvalida(DataException):
    """
    Excecao para quando os anos da data forem inválidos
    """


class MesInvalido(DataException):
    """
    Excecao para quando o mes da data for inválido
    """


class DiaInvalido(DataException):
    """
    Excecao para caso o dia da data seja inválido
    """


# --------------------------------------------------------------------------------------------- #


class CPFException(Exception):
    """
    Exceção pai para exceções HTTP 400 de CPF
    """


class CPFJaCadastrado(CPFException):
    """
    Excecao para quando o CPF do cliente ja estiver cadastrado
    """


class TamanhoCPF(CPFException):
    """
    Excecao para quando o tamanho do CPF ultrapassar 11 caracteres
    """


# --------------------------------------------------------------------------------------------- #


class ClienteException(Exception):
    """
    Excecao pai para as excecoes do Cliente
    """


class ClienteNaoEncontrado(ClienteException):
    """
    Excecao para quando o ID do cliente nao for encontrado
    """


class NomeInvalido(ClienteException):
    """
    Excecao para quando o nome do cliente for invalido
    """


class FormatoInfo(ClienteException):
    """
    Excecao para quando as inf. adicionais do cliente forem inválidas (conter espaços ou + de 30 caracteres)
    """


# --------------------------------------------------------------------------------------------- #


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


class DescricaoInvalida(ProdutoException):
    """
    Excecao para quando a descricao inserida for invalida
    """
    
class ProdutoNaoEncontrado(ProdutoException):
    """
    Excecao para quando o produto nao for encontrado
    """
