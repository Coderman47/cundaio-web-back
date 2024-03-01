# Service Layer
from repositories import QuestionRepository
import json


class QuestionService:
    def __init__(self):
        self.question_repository = QuestionRepository()
    
    def create_questions_from_message(self, message):
        questions = []
        if message.user_id is None and message.content_type == "json":
            message_data = json.loads(message.raw_content)
            for question_content in message_data.get('questions'):
                questions.append(self.question_repository.create({
                    'content': question_content,
                    'message_id': message.message_id
                }))
        return questions