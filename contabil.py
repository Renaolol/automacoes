class LanctoContabil:
    '''
    Classe que representa um lançamento contabil.

    Atributos:
        valor(float): O valor do lançamento contábil
        debito(int): código da conta contábil de débito
        credit(int): código da conta contábil de crédito
    '''

    def __init__(self,valor,debito,credito,historico):
        '''
        Inicia a classe
        '''
        self.valor=valor
        self.debito=debito
        self.credito=credito
        self.historico=historico
    def gera_lancto_dominio():
        return ""