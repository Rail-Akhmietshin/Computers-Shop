from .models import User
from .tasks import send_verification_email
from django.db.models import signals

def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_confirmation:
        send_verification_email.delay(instance.id)

signals.post_save.connect(user_post_save, sender=User)