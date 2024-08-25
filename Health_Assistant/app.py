import openai
import re
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify,render_template


# # Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']


# Initialize Flask app
app = Flask(__name__)

       
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

def get_response(messages):
    '''This function is responsible to generate the GPT responses'''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",temperature = 0.1,
        messages=messages
    )
    return response['choices'][0]['message']['content']



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    global messages
    try:
        data = request.json
        user_input = data.get("user_input")
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400
 
        messages = update_chat(messages, "user", user_input)
        # Get the response from the assistant function
        response = get_response(messages)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
