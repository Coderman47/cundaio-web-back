from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from repositories import UserRepository

#API
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)

#Logs
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")


@app.post('/register')
@tracer.capture_method
def register_user():
    try:
        user_data = app.current_event.json_body
        user = UserRepository().create(user_data)

        return {'message': 'User succesfully created'}

    except (ValueError, TypeError) as ve:
        return {'error': str(ve)}, 422
    except Exception as e:
        return {'error': str(e)}, 500


@app.post('/login')
@tracer.capture_method
def login_user():
    try:
        login_data = app.current_event.json_body
        token = UserRepository().login(login_data)

        return {'message': 'Login succesful', 'token': token}

    except (ValueError, TypeError) as e:
        return {'error': str(e)}, 422
    except Exception as e:
        return {'error': str(e)}, 500


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)