import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from model import Pessoa, Endereco, db_string

engine = create_engine(db_string, echo=True)
Session = sessionmaker(bind=engine)
s = Session()


def lambda_handler(event, context):
    data = s.query(Pessoa.genero, func.count(Pessoa.genero)).group_by(Pessoa.genero).all()
    data = {k: v for k, v in data}
    return {
        "statusCode": 200,
        "body": json.dumps(data),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
