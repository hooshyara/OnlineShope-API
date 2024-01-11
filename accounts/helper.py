from .models import User
from random import randint
import datetime
import jwt


def get_user(token):
    try:
        payload = jwt.decode(str(token), options={"verify_signature": False})
        print(payload['user_id'])
        user = User.objects.get(id=payload['user_id'])
        return user
    except:
        return None


def send_otp(mobile, otp):
    mobile = [mobile, ]


def get_random_otp():
    return randint(1000, 9999)


def check_otp_expiration(mobile):
    try:
        user = User.objects.get(mobile=mobile)
        now = datetime.datetime.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        if diff_time.seconds > 30:
            return False
        return True
    except User.DoesNotExist:
        return False
