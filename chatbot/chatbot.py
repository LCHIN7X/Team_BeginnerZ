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

# get groq API key from environment variable
groq_api_key = "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"

if not groq_api_key:
    raise ValueError("Groq API key not found. Please set the 'GROQ_API_KEY' environment variable.")

# initialize groq langchain chat object
groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192')

# initialize conversation memory
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

@chatbot.route("/chat", methods=["GET"])
def chat():
    return render_template("chat.html")

@chatbot.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"]

    # construct a chat prompt template using various components
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]
    )
    
    # create a conversation chain 
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )

    # generate chatbots answer by sending the full prompt to API
    response = conversation.predict(human_input=user_question)
    memory.save_context({'input': user_question}, {'output': response})

    formatted_response = format_response(response)

    return jsonify({"response": formatted_response})

def format_response(response):
    # limit the response to around 5 points
    points = response.split('\n')
    if len(points) > 5:
        points = points[:5]
    return '<br>'.join(points)

class ChatGroq:
    def __init__(self, groq_api_key, model_name):
        self.groq_api_key = groq_api_key
        self.model_name = model_name

    def get_recommendations(self, stock_data):
        recommendations = {}
        for stock in stock_data:
            # recommendation based on stock price
            if stock['price'] < 100:
                recommendations[stock['company']] = "Strong Buy"
            elif 100 <= stock['price'] < 200:
                recommendations[stock['company']] = "Buy"
            else:
                recommendations[stock['company']] = "Hold" 
        return recommendations

        



