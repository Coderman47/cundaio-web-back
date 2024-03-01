from sqlalchemy.orm import Session
import database
from models import User, Thread, ThreadUser, Message, Question, Base
from schemas import UserCreate, UserLogin, ThreadCreate, MessageCreate, QuestionCreate
from datetime import datetime
import json

engine = database.connection()
Base.metadata.create_all(engine)

# repositories abstract DB interation
class BaseRepository():
    def __init__(self, model):
        self.model = model

    def create(self, model_data):
        with Session(engine) as session:
            instance = self.model(**model_data)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def create(self, user_data):
        user_create_data = UserCreate(**user_data)
        user = super().create(user_data)
        if "user_id" not in user_data:
            self.create_token(user)
        return user
    
    def create_token(self, user):
        with Session(engine) as session:
            user.create_token()
            session.add(user)
            session.commit()
            session.refresh(user)
    
    def login(self, input_data):
        login_data = UserLogin(**input_data)
        with Session(engine) as session:
            user = session.query(User).filter_by(email=login_data.email).first()
            if user and user.password_is_valid(login_data.password):
                return user.token
            else:
                raise ValueError("Email or password are incorrect")
    
    
class ThreadRepository(BaseRepository):
    def __init__(self):
        super().__init__(Thread)

    def create(self, thread_data):
        with Session(engine) as session:
            # Validate the existence of the user
            user = session.query(User).filter_by(user_id=thread_data.get('user_id')).first()
            if not user:
                raise ValueError("User not found")

            # Create a new thread instance
            new_thread = Thread(
                instructions=thread_data.get('instructions'),
                openai_assistant_id=thread_data.get('openai_assistant_id'),
                openai_thread_id=thread_data.get('openai_thread_id'),
            )

            # Link the thread and user
            thread_user = ThreadUser(user=user)

            # Add thread and thread_user to the session
            new_thread.users.append(thread_user)
            session.add(new_thread)
            session.commit()
            session.refresh(new_thread)

            return new_thread
    
    def get_thread(self, thread_id):
        with Session(engine) as session:
            thread = session.query(Thread).filter_by(thread_id=thread_id).first()
            return thread
    
    def get_user_threads(self, user_id):
        with Session(engine) as session:
            threads = session.query(Thread).join(ThreadUser).filter(ThreadUser.user_id == user_id).all()
            return threads

    def get_thread_messages(self, thread_id):
        with Session(engine) as session:
            messages = session.query(Message).filter_by(thread_id=thread_id).all()
            return messages


class MessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(Message)

    def create(self, message_data):
        with Session(engine) as session:
            # Validate the existence of the thread
            thread = session.query(Thread).filter_by(thread_id=message_data.get('thread_id')).first()
            if not thread:
                raise ValueError("Thread not found")

            # Create a new message instance
            new_message = Message(raw_content=message_data.get('content'), user_id=message_data.get('user_id'), timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            try:
                new_message.content = json.loads(new_message.raw_content).get('answer')
            except json.JSONDecodeError:
                new_message.content = new_message.raw_content
                new_message.content_type = "text"
            else:
                new_message.content_type = "json"

            # Link the message and thread
            new_message.thread = thread

            # Add message and thread to the session
            session.add(new_message)
            session.commit()
            session.refresh(new_message)

            return new_message

class QuestionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Question)

    def create(self, question_data):
        with Session(engine) as session:
            # Validate the existence of the message
            message = session.query(Message).filter_by(message_id=question_data.get('message_id')).first()
            if not message:
                raise ValueError("Message not found")

            # Create a new question instance
            new_question = Question(content=question_data.get('content'), message_id=question_data.get('message_id'), timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Link the question and message
            new_question.message = message

            # Add question and thread to the session
            session.add(new_question)
            session.commit()
            session.refresh(new_question)

            return new_question

    def answer_question(self, question_id, answer_text):
        with Session(engine) as session:
            # Validate the existence of the question
            question = session.query(Question).filter_by(question_id=question_id).first()
            if not question:
                raise ValueError("Question not found")

            # Update the question's answer
            question.answer = answer_text

            # Add the updated question to the session
            session.add(question)
            session.commit()

            return question
