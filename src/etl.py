import requests
import json
import collections
from difflib import SequenceMatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base64 import b64encode
from datetime import datetime

import boto3

from model import Pessoa, Endereco, db_string


# Flatten nested dictionaries
# https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
# i do this because is more easy to search the keys without crazy nested loops
def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Join columns table names, to be more precisely i compare with strings like the keys, with keys from json
# i measure the distance between these two string (cited before line)
# in future i can use more sophisticated function from NPL domain (AI or machine learning)
# This is interesting because is not more needed manually to map input data to table columns
# But is necessary feed the this function with data
def join_data(dict_out, dict_in):
    join_dict = dict_out.copy()
    for key_out, value_out in list(dict_out.items()):
        for value in list(value_out.keys()):
            for key_in, value_in in list(dict_in.items()):
                ratio = similar(value, key_in)
                if ratio > .99:
                    #value_out[v] = value_in
                    join_dict[key_out][key_in] = value_in
    return join_dict

# string similaty function
#https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Compare
def clean_dict(dict_in, out_dict):
    for key, value in dict_in.items():
        list_string = []
        for k, v in value.items():
            if k != '':
                list_string.append(str(v))
        out_dict[key] = ''.join(list_string)
    return out_dict


def lambda_handler(event, context):
    # table column names
    person_keys = ['nome_completo', 'email', 'username', 'password', 'genero', 'photo']
    # names where i will use the similarity function
    # These names are the same from that we get flatted dicts
    person_keys_words = [['name_first', 'name_last'], ['email'], ['login_username'], ['login_password'], ['gender'], ['picture_large']]
    person = dict.fromkeys(person_keys, None)
    person_search = {}
    # now i nest boot dicts, each column name with yours keys
    # i do the same with address data
    for key, value in zip(person_keys, person_keys_words):
        person_search[key] = {}
        for v in value:
            person_search[key][v] = {}

    address_keys = ['rua', 'numero', 'cidade', 'estado']
    address_keys_words = [['location_street_name'], ['location_street_number'], ['location_city'], ['location_state']]
    address = dict.fromkeys(address_keys, None)
    address_search = {}
    for key, value in zip(address_keys, address_keys_words):
        address_search[key] = {}
        for v in value:
            address_search[key][v] = {}


    # get data from API
    response = requests.get('https://randomuser.me/api/')
    json_data = json.loads(response.text)
    user_data = json_data['results'][0]
    # flat json data
    user_data_flatt = flatten(user_data)

    person_search = join_data(person_search, user_data_flatt)
    address_search = join_data(address_search, user_data_flatt)

    person_dict = clean_dict(person_search, person)
    address_dict = clean_dict(address_search, address)

    # get image data
    response = requests.get(person_dict["photo"])
    #response.raw.decode_content = True
    # convert to base to be possible to save in postgres
    person_dict["photo"] = b64encode(response.content)

    # create connection and session with database
    engine = create_engine(db_string, echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    pessoa = Pessoa(**person_dict)
    # add data and get get the instance primary key to be used as foreign key in address instance
    s.add(pessoa)
    s.flush()

    pessoa_id = pessoa.id
    address_dict["pessoa_id"] = pessoa.id
    endereco = Endereco(**address_dict)
    s.add(endereco)
    s.commit()
    s.close()

    # save raw data in s3 bucket, this ios important to data scientists and machine learning engineers
    bucket_name = "rbs-case"
    file_name = str(pessoa_id) + ".json"
    s3_path = "randomuser/" + file_name

    s3 = boto3.resource("s3")
    json_data["aquisition_date"] = "{:%Y%m%d_%H%M%s}".format(datetime.now())
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=bytes(json.dumps(json_data).encode('UTF-8')))
    # TODO add return data
