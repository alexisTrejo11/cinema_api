import os
from celery import Celery

# Configurar Celery con Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment.settings')

app = Celery('payment')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
