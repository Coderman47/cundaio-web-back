from typing import List
from sqlalchemy import Column, Integer, String, UniqueConstraint, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.event import listens_for
import bcrypt
from datetime import datetime, timedelta
import jwt
import os


# SQLAlchemy models
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    given_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    corpoweb: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(Text, nullable=True)
    threads: Mapped[List["ThreadUser"]] = relationship(back_populates="user")
    messages: Mapped[List["Message"]] = relationship(back_populates="user")

    __table_args__ = (
        UniqueConstraint('email', name='user_email_unique'),
    )

    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def create_token(self):
        payload = {
            "iat": datetime.utcnow(),
            #"exp": datetime.utcnow() + timedelta(days=5),
            "sub": "user",
            "user_id": self.user_id,
            "user_fields": {
                "date_joined": str(datetime.now().replace(microsecond=0))
            }
        }
        self.token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
    
    def password_is_valid(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


@listens_for(User, 'before_insert')
def hash_password_event(mapper, connection, target):
    if target.password:
        target.hash_password(target.password)

class Thread(Base):
    __tablename__ = "threads"

    thread_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instructions: Mapped[str] = mapped_column(Text, nullable=True)
    openai_assistant_id: Mapped[str] = mapped_column(String(255), nullable=True)
    openai_thread_id: Mapped[str] = mapped_column(String(255), nullable=True)
    users: Mapped[List["ThreadUser"]] = relationship(back_populates="thread")
    messages: Mapped[List["Message"]] = relationship(back_populates="thread")

class ThreadUser(Base):
    __tablename__ = "thread_users"

    thread_user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.thread_id"), nullable=False)
    thread: Mapped["Thread"] = relationship(back_populates="users")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="threads")

    __table_args__ = (
        UniqueConstraint('thread_id', 'user_id', name='thread_user_unique'),
    )

class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.thread_id"), nullable=False)
    thread: Mapped["Thread"] = relationship()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    user: Mapped["User"] = relationship()
    content: Mapped[str] = mapped_column(Text, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[str] = mapped_column(String(255), nullable=False)
    questions: Mapped[List["Question"]] = relationship(back_populates="message")

    def role(self):
        return "user" if self.user_id is not None else "agent"

class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(255), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.message_id"), nullable=False)
    message: Mapped["Message"] = relationship()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    user: Mapped["User"] = relationship()