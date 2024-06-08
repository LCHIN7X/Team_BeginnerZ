from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
from user.models import User
from flask_login import current_user, login_required
from models import db

load_dotenv()

quiz = Blueprint('quiz',__name__,template_folder='templates',static_folder='static')
QUIZ_LENGTH = 5
API_KEY = os.getenv('API_KEY')
client = Groq(api_key=API_KEY)

# functions to get quiz questions from API 
def get_questions_from_api():
    questions = []

    for _ in range(QUIZ_LENGTH):
        prompt = """Generate a multiple-choice question regarding finances, with the goal of educating the user and increasing their financial literacy. 
        Format each question like so: 
        Question: <question text> \n A) <option A> \n B) <option B> \n C) <option C> \n Correct answer: <correct answer, including option text>. 
        Only include the question, question selections and the answer, nothing else. 
        Every answer option must be valid and not None."""
        chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": 'system',
                        'content': 'Assume the role of a financial expert.'
                    },
                    {
                        "role": 'user',
                        'content': prompt
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
    correct_answer = None

    for line in lines[1:]:
        if line.strip().startswith('A)'):
            options['option_a'] = line.strip()
        elif line.strip().startswith('B)'):
            options["option_b"] = line.strip()
        elif line.strip().startswith('C)'):
            options["option_c"] = line.strip()
        elif line.strip().startswith('Correct answer:'):
            line = line.strip()
            correct_answer = line.replace('Correct answer:', '').strip()
    
    return question, options.get('option_a'), options.get('option_b'), options.get('option_c'), correct_answer


@quiz.route('/generate-explanation', methods=['POST'])
def generate_explanation():
    data = request.get_json()
    question = data.get('question')
    user_answer = data.get('user_answer')
    correct_answer = data.get('correct_answer')
    option_a = data.get('option_a')
    option_b = data.get('option_b')
    option_c = data.get('option_c')

    explanation_prompt = f"""
    Consider the question below, and the answer options.
    Question: {question}
    Options:
    A) {option_a}
    B) {option_b}
    C) {option_c}
    User's Answer: {user_answer}
    Correct Answer: {correct_answer}
    If the user's answer was wrong, please provide an explanation for why the correct answer is correct and why the user's answer is incorrect.
    If the user's answer was correct, also provide an explanation to elaborate more on why the other 2 answers are incorrect.
    Respond as if you are talking to the user one-on-one. An explanation must be generated for each prompt. Only provide the explanation, nothing else.
    """

    answers_chat = client.chat.completions.create(
                messages=[
                    {
                        "role": 'system',
                        'content': 'Assume the role of a financial expert who is also very good at teaching laymen technical finance knowledge.'
                    },
                    {
                        "role": 'user',
                        'content': explanation_prompt
                    }
                ],
                model="llama3-8b-8192",
            )

    explanation = answers_chat.choices[0].message.content
    return jsonify({'explanation': explanation})

    

# routes for 'quiz' blueprint
@quiz.route('/take_quiz',methods=["GET"])
@login_required
def quiz_page():        
    cash = current_user.cash
    return render_template('quiz.html',cash=cash)


@quiz.route('/get-questions',methods=['GET'])
@login_required
def get_questions():
    questions = get_questions_from_api()
    print(questions)
    # output for print(questions) 
    # [{'question': 'Question: What is the primary purpose of a 401(k) plan?', 'option_a': ' A) To provide immediate access to your retirement savings', 'option_b': ' B) To reduce your taxable income', 'option_c': ' C) To save for retirement', 'answer': 'C)'}, 
    # {'question': 'Question: What is the main purpose of compound interest in a savings account?', 'option_a': ' A) To save a fixed amount of money in a short period of time', 'option_b': ' B) To earn interest on interest over time', 'option_c': ' C) To prevent market fluctuations', 'answer': 'B) To earn interest on interest over time'}, {'question': 'Question: What is a mutual fund?', 'option_a': ' A) A type of life insurance policy', 'option_b': ' B) A professionally managed investment portfolio that pools money from many investors', 'option_c': ' C) A type of retirement account', 'answer': 'B)'}, {'question': 'Question: When evaluating the expenses of your daily expenses, which of the following is True?', 'option_a': 'A) Fixed expenses are expenses that can vary from month to month.', 'option_b': 'B) Fixed expenses are expenses that remain constant every month.', 'option_c': 'C) Fixed expenses are expenses that can be easily cut back on.', 'answer': 'B)'}, {'question': 'Question: What is the term for the amount of money required to buy something, especially an asset or an investment?', 'option_a': ' A) Value', 'option_b': ' B) Value at Risk (VaR)', 'option_c': ' C) Appreciation', 'answer': 'B) Value at Risk (VaR)'}, {'question': 'Question: What is the main purpose of a budget?', 'option_a': ' A) To track and manage income and expenses', 'option_b': ' B) To invest money for long-term growth', 'option_c': ' C) To save a certain amount of money', 'answer': 'A)'}, {'question': 'Question: What happens to the purchasing power of money over time due to inflation?', 'option_a': 'A) It increases', 'option_b': 'B) It remains the same', 'option_c': 'C) It decreases', 'answer': 'C) It decreases'}, {'question': "Question: What is the net effect on an individual's credit score when a credit card payment is made in full each month?", 'option_a': 'A) The payment has no effect on the credit score.', 'option_b': 'B) The payment increases the credit score because it shows responsible financial behavior.', 'option_c': 'C) The payment decreases the credit score because it implies a reduced credit utilization ratio.', 'answer': 'B) The payment increases the credit score because it shows responsible financial behavior.'}, {'question': 'Question: What is the main purpose of dollar-cost averaging in investing?', 'option_a': 'A) To take on high levels of risk to potentially earn higher returns', 'option_b': "B) To invest a fixed amount of money at regular intervals, regardless of the market's performance", 'option_c': 'C) To diversify a portfolio by investing in a variety of different asset classes', 'answer': 'B)'}, {'question': 'Question: What is the main purpose of having an emergency fund?', 'option_a': 'A) To invest in the stock market', 'option_b': 'B) To pay off high-interest debt', 'option_c': 'C) To cover 3-6 months of essential expenses in case of unexpected events', 'answer': 'C)'}]
    return jsonify({'questions' : questions}) 


@quiz.route('/increment-cash')
@login_required
def increment_cash():
    current_user.cash += 5.00
    db.session.commit()


    return jsonify({'message' : 'success'})