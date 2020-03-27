from sqlalchemy import create_engine
from model import Base, Pessoa, Endereco, db_string

# function to create tables in database

#db_string = "postgres://postgres:postgres@rbs.c1iklbtaxq8y.us-east-2.rds.amazonaws.com:5432/rbs"
engine = create_engine(db_string)
print(Pessoa)
print(Endereco)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)