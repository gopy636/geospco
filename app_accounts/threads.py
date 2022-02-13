import threading, random, uuid
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache

class send_verification_otp(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            otp = str(random.randint(100000, 999999))
            cache.set(otp, self.email, timeout=350)
            subject = "Link to verify the your Account"
            message = f"The OTP to verify your email is {otp}."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)
