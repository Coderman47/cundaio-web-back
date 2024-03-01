import jwt
import os
from typing import Any
from aws_lambda_powertools import Logger, Tracer, Metrics


#Logs
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")


@tracer.capture_lambda_handler
def lambda_handler(event: dict, context):
    try:
        decoded_token = jwt.decode(event['authorizationToken'], os.getenv('JWT_SECRET'), algorithms='HS256')
    except Exception as error:
        logger.error(f'Error: {str(error)}')
        return get_policy("Deny", event)
    policy = get_policy("Allow", event)
    policy["context"] = { 
        "token": event['authorizationToken'],
        "user_id": decoded_token["user_id"]
    }
    return policy


def get_policy_document(effect, resource) -> dict[str, Any]:
    return {
        "Version": "2012-10-17",
        "Statement": [
            { "Action": "execute-api:Invoke", "Effect": effect, "Resource": resource }
        ],
    }


def get_policy(effect, event) -> dict[str, Any]:
    return {
        "principalId": "user",
        "policyDocument": get_policy_document(
            effect=effect, resource=event["methodArn"]
        ),
        "context": { "message": "Unauthorized" },
    }
    
