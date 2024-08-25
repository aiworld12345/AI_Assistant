import openai
import re
import os
from dotenv import load_dotenv, find_dotenv


# # Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

messages = [
    {"role": "system", "content": """You are a virtual health assistant designed to help users understand their symptoms and provide basic non-diagnostic advice. 
    if the the user says hi or hello you need to tell about your role.
    You are not a substitute for professional medical advice, diagnosis, or treatment. Your role is to  ask the user to describe their symptoms in detail.
    Based on the user's input, provide general information about potential causes of the symptoms, emphasizing that these are possibilities, not diagnoses.
    Suggest non-prescription remedies that are commonly used for the symptoms described and advise the user to consult a healthcare professional before taking any new medication or if symptoms persist or worsen.
    whenever user greets you saying hi or hello greet them back and tell what you are and how you can help them"""}
]


def update_chat(messages, role, content):
    '''This function add the previous message and maintain the chat history'''
    messages.append({"role": role, "content": content})
    return messages

def get_chatgpt_response(messages):
    '''This function is responsible to generate the GPT responses'''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",temperature = 0.1,
        messages=messages
    )
    return response['choices'][0]['message']['content']



while True:

    user_input = input("user query: ")
    messages = update_chat(messages, "user", user_input)
    model_response = get_chatgpt_response(messages)
    print(model_response)

