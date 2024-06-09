from flask import Blueprint, render_template,request
from flask_login import login_required
from chatbot.chatbot import ChatGroq


lesson = Blueprint("lesson", __name__, template_folder="templates", static_folder="static")

@lesson.route("/HTML_PAGE_1")
@login_required
def lesson_page1():
    return render_template("HTML_PAGE_1.html")

@lesson.route("/HTML_PAGE_2")
@login_required
def lesson_page2():
    return render_template("HTML_PAGE_2.html")

@lesson.route("/HTML_PAGE_3")
@login_required
def lesson_page3():
    return render_template("HTML_PAGE_3.html")

@lesson.route("/HTML_PAGE_4")
@login_required
def lesson_page4():
    return render_template("HTML_PAGE_4.html")

@lesson.route("/HTML_PAGE_5")
@login_required
def lesson_page5():
    return render_template("HTML_PAGE_5.html")


@lesson.route("HTML_PAGE_6")
@login_required
def lesson_page6():
    return render_template("HTML_PAGE_6.html")

@lesson.route("/HTML_PAGE_7")
@login_required
def lesson_page7():
    return render_template("HTML_PAGE_7.html")

@lesson.route("/HTML_PAGE_8")
@login_required
def lesson_page8():
    return render_template("HTML_PAGE_8.html")

@lesson.route("/HTML_PAGE_9")
@login_required
def lesson_page9():
    return render_template("HTML_PAGE_9.html")

@lesson.route("/HTML_PAGE_10")
@login_required
def lesson_page10():
    return render_template("HTML_PAGE_10.html")

@lesson.route("/HTML_PAGE_11")
@login_required
def lesson_page11():
    return render_template("HTML_PAGE_11.html")

@lesson.route("/HTML_PAGE_12")
@login_required
def lesson_page12():
    return render_template("HTML_PAGE_12.html")

@lesson.route("/HTML_PAGE_13")
@login_required
def lesson_page13():
    return render_template("HTML_PAGE_13.html")

@lesson.route("/knowledge")
@login_required
def knowledge_page():
    groq_api_key = "a74c1d6a9bfc48a096826ab16608dd72"
    groq_instance = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192')

    # Generate knowledge content about finance
    topic = "finance"
    knowledge = groq_instance.generate_knowledge(topic)
    
    return render_template("knowledge.html", topic=topic, knowledge=knowledge)
