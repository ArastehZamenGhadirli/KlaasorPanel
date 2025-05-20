from celery import shared_task
from kavenegar import KavenegarAPI, APIException # type: ignore
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_sms_to_user(phone_number):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        message = f"درخواست شما برای ثبت نام بوت کمپ ثبت شد"
        params = {
            'sender': '2000660110',
            'receptor': '09209201592',
            'message': message,
        }
        response = api.sms_send(params)
        return response
    except APIException as e:
        return str(e)
    except Exception as e:
        return str(e)
    
@shared_task
def send_registration_email(email):
    subject = "ثبت‌نام بوت‌کمپ"
    message = "درخواست ثبت‌نام شما با موفقیت ثبت شد و در حال بررسی است."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return str(e)
    
