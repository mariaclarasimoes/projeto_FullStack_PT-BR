from pydantic import BaseModel
from typing import Optional, List
from model.empresa import Empresa

from schemas import ComentarioSchema


class EmpresaSchema(BaseModel):
    # Define como os campos devem ser representados ao inserir uma nova empresa
    
    nome_empresa: str = "Alpargatas S.A"
    nome_fantasia: str = "Havaianas"
    cnpj: str = "99.999.999/0001-99"
    nome_responsavel: str = "José da Silva"
    telefone: str = "() 99999-9999"
    email: str = "josedasilva@seuemail.com"

    
class EmpresaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca que será feita apenas com base no "nome_empresa" da Empresa. """
    
    nome_empresa: str = "Teste"


class ListagemEmpresasSchema(BaseModel):
    # Define como uma listagem de empresas será retornada.

    empresas:List[EmpresaSchema]


def apresenta_empresas(empresas: List[Empresa]):
    # Retorna a representação da empresa seguindo o schema definido em "EmpresaViewSchema".
  
    result = []
    for empresa in empresas:
        result.append({
            "nome_empresa": empresa.nome_empresa,
            "nome_fantasia": empresa.nome_fantasia,
            "cnpj": empresa.cnpj,
            "nome_responsavel": empresa.nome_responsavel,
            "telefone": empresa.telefone,
            "email": empresa.email
        })

    return {"empresas": result}


class EmpresaViewSchema(BaseModel):
    # Define como um produto será retornado: empresa + comentários

    id: int = 1
    nome_empresa: str = "Alpargatas S.A"
    nome_fantasia: str = "Havaianas"
    cnpj: str = "99.999.999/0001-99"
    nome_responsavel: str = "José da Silva"
    telefone: str = "() 99999-9999"
    email: str = "josedasilva@seuemail.com"
    total_comentarios: int = 1
    comentarios:List[ComentarioSchema]


class EmpresaDelSchema(BaseModel):
    # Define como deve ser a estrutura do dado retornado após uma requisição de remoção.

    mesage: str
    nome_empresa: str

def apresenta_empresa(empresa: Empresa):
    # Retorna uma representação da empresa seguindo o schema definido em EmpresaViewSchema.

    return {
        "id": empresa.id,
        "nome_empresa": empresa.nome_empresa,
        "nome_fantasia": empresa.nome_fantasia,
        "cnpj": empresa.cnpj,
        "nome_responsavel": empresa.nome_responsavel,
        "telefone": empresa.telefone,
        "email": empresa.email,
        "total_comentarios": len(empresa.comentarios),
        "comentarios": [{"texto": c.texto} for c in empresa.comentarios]
    }
