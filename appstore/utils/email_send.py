__author__ = 'Jeff'
__date__ = '2017/12/28 17:03'


from users.models import EmailVerifyRecord
import random, string
from django.core.mail import send_mail
from self_study.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '自学网注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def random_str(randomlength=8):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, randomlength))
    return salt