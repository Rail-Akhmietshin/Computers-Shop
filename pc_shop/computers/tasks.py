import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from pc_shop.celery import app
from  pc_shop.settings import EMAIL_HOST_USER

@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            subject=f'Подтверждение аккаунта "{user.number_phone}"',
            message=f"Для подтверждения аккаунта, перейдите по ссылке:\nhttp://localhost:1337{reverse('verify', kwargs={'uuid': str(user.verification_uuid)})}",
            from_email=EMAIL_HOST_USER,
	        recipient_list=[user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(f"Попытка отправить подтверждение аккаунта несуществующему пользователю '{user_id}'")
