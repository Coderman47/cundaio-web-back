import json
import os
from sqlalchemy import create_engine
from aws_lambda_powertools.utilities import parameters

#DB Connection
def connection():
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    db_secret = json.loads(parameters.get_secret(os.getenv('DB_SECRET')))
    username = db_secret.get("username")
    password = db_secret.get("password")
    
    db_url = f'postgresql://{username}:{password}@{db_host}/{db_name}'
    
    return create_engine(db_url)

