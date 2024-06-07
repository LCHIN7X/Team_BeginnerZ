from flask import Blueprint, render_template, redirect, url_for 

quiz = Blueprint('quiz',__name__,template_folder='templates',static_folder='static')


@quiz.route('/take_quiz')
def answer_quiz():
    return render_template('quiz.html')