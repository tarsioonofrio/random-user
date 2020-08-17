# Proposal

The client's business area requested that the user database be
enriched with data from a new source. Access to this data source is given
through the following API: https://randomuser.me/api/

### Introduction

The customer database is relational and has the following schema:

Pessoa 
id: long 
nome completo: string
email: string
username: string
password: string
genero: string 
photho: blob

Endereco
id: long
pessoa_id: long
rua: string
numero: string
cidade: string
genero: string
estado: string

### Deliverables

You should:
1. Write a service that, once a minute, consult the API previously
mentioned and the data received according to the RBS basis persists.
2. Write a query to the Company's BI team that delivers the number of
users by gender and city.
3. Present in a personal interview, in a generic way, how the case relates to
the challenges of building a data lake / dw and the concept of scalability.

### Recommendations

• You must write code in Java, Kotlin or Python that implements the flow of
data described.
• To make data persist, we recommend uploading a docker with the database
Dice.
• It will be evaluated in your code: clean code, tests, logic.

## Requirements

Install the requirements:
pip install sqlalchemy requests psycopg2

The Linux AMI, image used in AWS Lambda, doesn't have installed postgres client
Beacause that this repo is necessary   
git clone https://github.com/jkehler/awslambda-psycopg2

## TODO

Add tests and refactor the code

