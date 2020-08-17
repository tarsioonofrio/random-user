from sqlalchemy import create_engine
from model import Base, Pessoa, Endereco, db_string

# function to create tables in database

engine = create_engine(db_string)
print(Pessoa)
print(Endereco)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)