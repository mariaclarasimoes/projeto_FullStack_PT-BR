from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario

class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column("pk_empresa", Integer, primary_key=True)
    nome_empresa = Column(String(140), unique=True)
    nome_fantasia = Column(String(140))
    cnpj = Column(String(18))
    nome_responsavel = Column(String(100))
    telefone = Column(String(15))
    email = Column(String(100))
    data_insercao = Column(DateTime, default=datetime.now())

    """ Definição do relacionamento entre a empresa e o comentário.
    A relação é implicita e não está salva na tabela 'empresa', fica a responsabilidade do SQLAlchemy de reconstruir esse relacionamento. """
    comentarios = relationship("Comentario")

    def __init__(self, nome_empresa:str, nome_fantasia:str, cnpj:str, nome_responsavel:str, telefone:str, email:str,
                 data_insercao:Union[DateTime, None] = None):
        """ Cria um empresa

        Arguments:
            *nome_empresa: nome da empresa.
            *nome_fantasia: nome fantasia da empresa.
            *cnpj: CNPJ da empresa.
            *nome_responsavel: Nome do responsável pelo contato na empresa
            *telefone: Telefone de contato da empresa
            *email: Email de contato da empresa 
            *data_insercao: data de quando o empresa foi inserido à base
        """
        self.nome_empresa = nome_empresa
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj
        self.nome_responsavel = nome_responsavel
        self.telefone = telefone
        self.email = email

        # Se a data não for informada, será o data exata da inserção no banco.
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário à empresa """
        self.comentarios.append(comentario)

