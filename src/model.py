from sqlalchemy import Table, Column, String, MetaData, Integer, Binary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

db_string = "postgres://postgres:postgresrbs123@rbs.c1iklbtaxq8y.us-east-2.rds.amazonaws.com:5432/rbs"
Base = declarative_base()


class Pessoa(Base):
    __tablename__ = "pessoa"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String, nullable=False)
    email = Column(String, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    genero = Column(String, nullable=True)
    photo = Column(Binary, nullable=True)


class Endereco(Base):
    __tablename__ = "endereco"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pessoa_id = Column(Integer, ForeignKey(Pessoa.id))
    rua = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    genero = Column(String, nullable=True)
    estado = Column(String, nullable=True)

