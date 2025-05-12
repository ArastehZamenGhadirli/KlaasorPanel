from celery import shared_task
from kavenegar import KavenegarAPI, APIException # type: ignore
from django.conf import settings


@shared_task
def send_sms_to_user(phone_number, otp):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        message = f"کد تایید شما: {otp}"
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