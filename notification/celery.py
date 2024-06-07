from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        'send-daily-emails': {
            'task': 'tasks.send_daily_emails',
            'schedule': crontab(hour=12, minute=0),  
        },
    }
    return celery
