from flask import Blueprint, render_template

lesson = Blueprint("lesson", __name__, template_folder="templates", static_folder="static")

@lesson.route("/lesson2")
def lesson_page():
    return render_template("lesson2.html")

