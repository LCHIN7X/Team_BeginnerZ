from celery import Celery
from flask_mail import Message
from . import create_app, mail
from models import db
from user.models import User

celery = Celery(__name__)

app = create_app()
app.app_context().push()

@celery.task
def send_daily_emails():
    users = User.query.all()
    for user in users:
        msg = Message("Daily Update",
                      recipients=[user.email])
        msg.body = "Here is your daily update!"
        mail.send(msg)
