from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from repositories import ThreadRepository, MessageRepository
from services import QuestionService
from llm import Assistant

#API
cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)

#Logs
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")


@app.post("/threads/new")
@tracer.capture_method
def new_thread():
    authorizer_context = app.current_event.request_context.authorizer
    thread_data = app.current_event.json_body
    assistant = Assistant(instructions=thread_data.get('instructions'))

    thread_data.update({
        "user_id": authorizer_context.get('user_id'),
        "openai_assistant_id": assistant.assistant_id,
        "openai_thread_id": assistant.create_thread()
    })

    thread = ThreadRepository().create(thread_data)

    return {"message": "Thread created successfully", "thread_id": thread.thread_id}


@app.get("/threads")
@tracer.capture_method
def get_threads():
    print('get_threads')
    authorizer_context = app.current_event.request_context.authorizer

    threads = ThreadRepository().get_user_threads(authorizer_context.get('user_id'))

    return {"threads": [{
            "id": thread.thread_id, 
            "instructions": thread.instructions
        } for thread in threads]}


@app.get("/threads/<thread_id>/messages")
@tracer.capture_method
def get_thread_messages(thread_id):
    messages = ThreadRepository().get_thread_messages(thread_id)

    return {"messages": [{
            "id": message.message_id,
            "message": message.content,
        } for message in messages]}


@app.post("/threads/<thread_id>/messages/new")
@tracer.capture_method
def new_thread_message(thread_id):
    authorizer_context = app.current_event.request_context.authorizer
    user_message_data = app.current_event.json_body # {"message": "Hello, how are you?"}
    user_message_data.update({"thread_id": thread_id, "user_id": authorizer_context.get('user_id')})
    message_repository = MessageRepository()
    user_message = message_repository.create(user_message_data)
    thread_repository = ThreadRepository()
    thread = thread_repository.get_thread(thread_id)

    assistant = Assistant(
        assistant_id=thread.openai_assistant_id, 
        thread_id=thread.openai_thread_id
    )
    assistant.create_message(user_message.content)
    agent_response = assistant.blocking_run()
    agent_message_data = {"thread_id": thread_id, "content": agent_response}
    agent_message = message_repository.create(agent_message_data)
    questions = QuestionService().create_questions_from_message(agent_message)

    return {
        "user": {
            "id": user_message.message_id, 
            "content": user_message.content
        },
        "agent": {
            "id": agent_message.message_id, 
            "content": agent_message.content,
            "questions": [{
                'id': question.question_id,
                'content': question.content,
            } for question in questions]
        }
    }


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)