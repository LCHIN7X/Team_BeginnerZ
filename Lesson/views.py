from flask import Blueprint, render_template

lesson = Blueprint("lesson", __name__, template_folder="templates", static_folder="static")

@lesson.route("/lesson")
def lesson_page():
    return render_template("page1.html")

