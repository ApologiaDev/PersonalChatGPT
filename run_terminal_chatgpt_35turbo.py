
import os

import openai
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv('OPENAIKEY')


class MessageHistory:
    def __init__(self, init_message={'role': 'system', 'content': 'You are a helpful and kind AI Assistant.'}):
        self.messages = [init_message]

    def get_messages(self):
        return self.messages

    def add_user_text(self, text):
        self.messages.append({
            'role': 'user',
            'content': text
        })

    def add_bot_reply(self, reply):
        self.messages.append({
            'role': 'assistant',
            'content': reply
        })


def get_reply(text, history):
    history.add_user_text(text)
    chat = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=history.get_messages()
    )
    reply = chat.choices[0].message.content
    history.add_bot_reply(reply)
    return reply


if __name__ == '__main__':
    history = MessageHistory()

    done = False
    while not done:
        inputtext = input('Prompt> ')
        if len(inputtext.strip()) == 0:
            done = True
        else:
            reply = get_reply(inputtext, history)
            print(reply)
            print("=====")
