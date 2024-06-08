import os
from flask import Blueprint, render_template, request, jsonify
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

chatbot = Blueprint("chatbot", __name__, template_folder="templates", static_folder="static")

# Get Groq API key from environment variable
groq_api_key = "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"

if not groq_api_key:
    raise ValueError("Groq API key not found. Please set the 'GROQ_API_KEY' environment variable.")

# Initialize Groq Langchain chat object
groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192')

# Initialize conversation memory
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

@chatbot.route("/chat", methods=["GET"])
def chat():
    return render_template("chat.html")

@chatbot.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"]

    # Construct a chat prompt template using various components
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]
    )
    
    # Create a conversation chain using the LangChain LLM (Language Learning Model)
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )

    # Generate the chatbot's answer by sending the full prompt to the Groq API
    response = conversation.predict(human_input=user_question)
    memory.save_context({'input': user_question}, {'output': response})

    formatted_response = format_response(response)

    return jsonify({"response": formatted_response})

def format_response(response):
    # Limit the response to around 5 points
    points = response.split('\n')
    if len(points) > 5:
        points = points[:5]
    return '<br>'.join(points)
