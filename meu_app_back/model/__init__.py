from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importa os elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.empresa import Empresa

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # Se não existe, cria o diretório
   os.makedirs(db_path)

# URL de acesso ao banco (essa é uma URL de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Cria o banco em caso de não existência 
if not database_exists(engine.url):
    create_database(engine.url) 

# Cria as tabelas do banco em caso de não existência
Base.metadata.create_all(engine)
