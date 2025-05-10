from celery import shared_task
from kavenegar import * # type: ignore
from kavenegar import KavenegarAPI, APIException # type: ignore
from django.conf import settings
@shared_task
def send_otp_sms(phone_number, otp_code):
    try:
        api = KavenegarAPI()  # Replace with real key
        message = f"Your verification code is: {otp_code}"
        params = { 'sender' : '2000660110', 'receptor': '09209201592', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
        response = api.sms_send(params)
        return response
    except APIException as e:
        return str(e)