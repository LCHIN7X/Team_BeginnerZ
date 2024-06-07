from flask import Blueprint, render_template, redirect, url_for, request

quiz = Blueprint('quiz',__name__,template_folder='templates',static_folder='static')


@quiz.route('/take_quiz',methods=["GET","POST"])
def quiz_page():
    if request.method == "POST":
        print("POST request successfully sent!")


    return render_template('quiz.html')