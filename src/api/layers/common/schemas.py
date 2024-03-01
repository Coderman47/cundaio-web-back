from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
import re


# Pydantic models for validation
class UserCreate(BaseModel):
    given_name: str
    last_name: str
    corpoweb: str
    email: EmailStr
    password: str

    @validator('password')
    def password_complexity(cls, value: str):
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        if not re.match(pattern, value):
            raise ValueError('Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character')
        return value

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    user_id: int
    given_name: str
    last_name: str
    corpoweb: str
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class ThreadCreate(BaseModel):
    user_id: int
    instructions: Optional[str] = None
    openai_assistant_id: Optional[int] = None
    openai_thread_id: Optional[int] = None

class Thread(BaseModel):
    thread_id: int
    instructions: Optional[str] = None
    openai_assistant_id: Optional[int] = None
    openai_thread_id: Optional[int] = None
    class Config:
        orm_mode = True

class ConversationCreate(BaseModel):
    user_id: int

class Conversation(BaseModel):
    conversation_id: int
    user_id: int
    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    conversation_id: int
    message: str
    timestamp: str

class Message(BaseModel):
    message_id: int
    conversation_id: int
    message: str
    timestamp: str
    class Config:
        orm_mode = True

class QuestionCreate(BaseModel):
    content: str
    timestamp: str

class Question(BaseModel):
    question_id: int
    content: str
    timestamp: str
    class Config:
        orm_mode = True