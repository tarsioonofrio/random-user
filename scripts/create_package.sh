#!/usr/bin/env bash

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
pip install --target ./src/aws-package sqlalchemy requests

# https://github.com/jkehler/awslambda-psycopg2
cp -r ./awslambda-psycopg2/psycopg2-3.7 ./src/aws-package/psycopg2

cd src
cd aws-package
zip -r9 ${OLDPWD}/aws-package.zip .
cd $OLDPWD

zip -g aws-package.zip *.py