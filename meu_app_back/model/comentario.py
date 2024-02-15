from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    """Definição do relacionamento entre o comentário e uma empresa.
    A coluna 'empresa' irá guardar a referencia à empresa, a chave estrangeira que relaciona uma empresa ao comentário. """
    empresa = Column(Integer, ForeignKey("empresa.pk_empresa"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """ Cria um Comentário
        Arguments:
            * Texto: o texto de um comentário.
            * Data_insercao: data de quando o comentário foi feito ou inserido à base """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
