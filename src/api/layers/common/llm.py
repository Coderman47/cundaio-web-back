import os
import json
from openai import OpenAI
import time

openai_api_key = os.getenv('OPENAI_API_KEY')


class Assistant:
    def __init__(self, **kwargs):
        self.openai_client = OpenAI(api_key=openai_api_key)
        instructions = kwargs.get('instructions')
        if instructions:
            self.assistant = self.openai_client.beta.assistants.create(
                instructions=instructions,
                name="Pre-sales Representative",
                model="gpt-4",
            )
            self.assistant_id = self.assistant.id
            self.thread = None
            self.thread_id = None
        else:
            self.assistant_id = kwargs.get('assistant_id')
            self.thread_id = kwargs.get('thread_id')
    
    def create_thread(self):
        self.thread = self.openai_client.beta.threads.create()
        self.thread_id = self.thread.id
        return self.thread.id
    
    def create_message(self, message):
        message = self.openai_client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=message
        )
        return message.id
    
    def create_run(self):
        run = self.openai_client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        return run.id
    
    def get_messages(self):
        messages = self.openai_client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        return messages.data
    
    def get_run_status(self, run_id):
        run_status = self.openai_client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run_id
        )
        return run_status.status
    
    def blocking_run(self):
        run_id = self.create_run()
        while True:
            # Run Check Status 
            run_check_status = self.get_run_status(run_id)
            if run_check_status == 'completed':
                messages = self.get_messages()
                break
            time.sleep(1) # to reduce bucle's loop
        print(messages)
        return messages[0].content[0].text.value
        
