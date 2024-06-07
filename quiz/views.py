from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

quiz = Blueprint('quiz',__name__,template_folder='templates',static_folder='static')
QUIZ_LENGTH = 10
API_KEY = os.getenv('API_KEY')
client = Groq(api_key=API_KEY)


# functions to get quiz questions from API 
def get_questions_from_api():
    questions = []

    for _ in range(QUIZ_LENGTH):
        chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": 'system',
                        'content': 'Assume the role of a financial expert.'
                    },
                    {
                        "role": 'user',
                        'content': "Generate a multiple-choice question regarding finances, with the goal of educating the user and increasing their financial literacy. Format each question like so: Question: <question text> \n A) <option A> \n B) <option B> \n C) <option C> \n Correct answer: <correct answer>. Only include the question, question selections and the answer, nothing else.",
                    }
                ],
                model="llama3-8b-8192",
            )
        question_content = chat_completion.choices[0].message.content
        question, option_a, option_b, option_c, correct_answer = extract_question_and_answer(question_content)
        questions.append({'question': question, 'option_a' : option_a, 'option_b' : option_b, 'option_c' : option_c, 'answer': correct_answer})

        return questions
        

def extract_question_and_answer(question_content):
    lines = question_content.split('\n')
    question = lines[0]

    options = {}

    for line in lines[1:]:
        if line.startswith('A)'):
            options['option_a'] = line 
        elif line.startswith('B)'):
            options["option_b"] = line 
        elif line.startswith('C)'):
            options["option_c"] = line 
        elif line.startswith('Correct answer:'):
            correct_answer = line.replace('Correct answer:', '').strip()
    
    return question, options.get('option_a'), options.get('option_b'), options.get('option_c'), correct_answer


# routes for 'quiz' blueprint
@quiz.route('/take_quiz',methods=["GET"])
def quiz_page():        
    return render_template('quiz.html')


@quiz.route('/get-questions',methods=['GET'])
def get_questions():
    questions = get_questions_from_api()
    print(questions)
    return jsonify({'questions' : questions})
