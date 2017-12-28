__author__ = 'Jeff'
__date__ = '2017/12/27 15:50'


from django.forms import Form, widgets
from django.forms import fields
from captcha.fields import CaptchaField


class Loginform(Form):
    username = fields.CharField(max_length=32,
                                required=True,
                                error_messages={
                                    'required': '用户名不能为空'
                                },
                                widget=widgets.TextInput(attrs={'class': "form-control", "placeholder": '用户名'}))
    password = fields.CharField(max_length=64,
                                required=True,
                                error_messages={
                                    'required': '密码不能为空'
                                },
                                widget=widgets.PasswordInput(attrs={'class': "form-control", "placeholder": '密码'}))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class RegisterForm(Form):
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})