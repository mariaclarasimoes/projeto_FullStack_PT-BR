from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Empresa, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição das tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
empresa_tag = Tag(name="Empresa", description="Adição, visualização e remoção de empresas à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um empresas cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    
    return redirect('/openapi')


@app.post('/empresa', tags=[empresa_tag],
          responses={"200": EmpresaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_empresa(form: EmpresaSchema):
    """Adiciona uma nova empresa à base de dados
    Retorna uma representação dos empresas e comentários associados. """

    empresa = Empresa(
        nome_empresa=form.nome_empresa,
        nome_fantasia=form.nome_fantasia,
        cnpj=form.cnpj,
        nome_responsavel= form.nome_responsavel,
        telefone= form.telefone,
        email=form.email
        )
    logger.debug(f"Adicionando uma empresa de nome: '{empresa.nome_empresa}'")
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando empresa
        session.add(empresa)
        # Efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado empresa de nome: '{empresa.nome_empresa}'")
        return apresenta_empresa(empresa), 200

    except IntegrityError as e:
        # A duplicidade do nome_empresa é provável razão do IntegrityError
        error_msg = "Empresa de mesmo nome já salvo na base"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome_empresa}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # Caso ocorra outro erro fora do previsto
        error_msg = "Não foi possível salvar novo item"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome_empresa}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/empresas', tags=[empresa_tag],
         responses={"200": ListagemEmpresasSchema, "404": ErrorSchema})
def get_empresas():
    """Faz a busca por todas as empresa cadastradas. 
    Retorna uma representação da listagem de empresas.
    """
    logger.debug(f"Coletando empresas ")
    # Cria uma conexão com a base
    session = Session()
    # Faz a busca
    empresas = session.query(Empresa).all()

    if not empresas:
        # Checa se não há empresas cadastradas
        return {"empresas": []}, 200
    else:
        logger.debug(f"%d Empresas encontradas: " % len(empresas))
        # Retorna a representação da empresa
        print(empresas)
        return apresenta_empresas(empresas), 200


@app.delete('/empresa', tags=[empresa_tag],
            responses={"200": EmpresaDelSchema, "404": ErrorSchema})
def del_empresa(query: EmpresaBuscaSchema):
    """Deleta uma empresa a partir do "nome_empresa" informado
    Retorna uma mensagem de confirmação da remoção. """
    empresa_nome_empresa = unquote(unquote(query.nome_empresa))
    print(empresa_nome_empresa)
    logger.debug(f"Deletando dados sobre a empresa #{empresa_nome_empresa}")

    # Criando conexão com a base
    session = Session()

    # Faz a remoção
    count = session.query(Empresa).filter(Empresa.nome_empresa == empresa_nome_empresa).delete()
    session.commit()

    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Empresa deletada: #{empresa_nome_empresa}")
        return {"mesage": "Empresa removida", "id": empresa_nome_empresa}
    else:
        # Se o empresa não foi encontrada
        error_msg = "Empresa não encontrada na base"
        logger.warning(f"Erro ao deletar empresa #'{empresa_nome_empresa}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": EmpresaViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona um novo comentário à empresa cadastrada na base identificado pelo id
    Retorna uma representação das empresas e comentários associados. """
    empresa_id  = form.empresa_id
    logger.debug(f"Adicionando comentários à empresa #{empresa_id}")

    # Criando conexão com a base
    session = Session()
    # Fazendo a busca pela empresa
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        # Se a empresa não for encontrada
        error_msg = "Empresa não encontrada na base"
        logger.warning(f"Erro ao adicionar comentário à empresa '{empresa_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # Criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # Adicionando comentário à empresa
    empresa.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário à empresa #{empresa_id}")

    # Retorna a representação da empresa
    return apresenta_empresa(empresa), 200
