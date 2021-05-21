# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/16 15:16
from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from user.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, required=True, error_messages={
        'required': '用户名必须输入',
        'min_length': '用户名至少三位',
    })
    password = forms.CharField(min_length=3, required=True, error_messages={
        'required': '密码必须输入',
        'min_length': '密码至少三位',
    })
    confirm = forms.CharField(min_length=3, required=True, error_messages={
        'required': '确认密码必须输入',
        'min_length': '密码至少三位',
    })
    email = forms.EmailField(required=True, error_messages={
        'required': '邮箱必须输入',
    })

    phone = forms.IntegerField(required=True, error_messages={
        'required': '电话必须输入',
    })

    sex = forms.IntegerField(required=True, error_messages={
        'required': '性别必须输入',
    })

    # 用户名验证
    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        users = User.objects.filter()
        for user in users:
            if username == user.username:
                raise ValidationError('用户名重复')
        return username

    # 单个字段验证
    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if password and password.isdigit():
            raise ValidationError('不能输入纯数字')
        return password

    # 全局验证 验证不止一个字段的值
    def clean(self):
        password = self.cleaned_data.get('password', None)
        confirm = self.cleaned_data.get('confirm', '')
        if password != confirm:
            raise ValidationError({'confirm': '两次输入密码不一致'})
        return self.cleaned_data


class ChangeForm(forms.Form):
    uid = forms.IntegerField()
    username = forms.CharField(min_length=3, required=True, error_messages={
        'required': '用户名必须输入',
        'min_length': '用户名至少三位',
    })
    email = forms.EmailField(required=True, error_messages={
        'required': '邮箱必须输入',
    })

    phone = forms.IntegerField(required=True, error_messages={
        'required': '电话必须输入',
    })

    sex = forms.IntegerField(required=True, error_messages={
        'required': '性别必须输入',
    })

    # 用户名验证
    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        uid = self.cleaned_data.get('uid', None)
        users = User.objects.filter()
        for user in users:
            if user.uid != uid:
                if username == user.username:
                    raise ValidationError('用户名重复')
        return username


class LoginCaptchaForm(forms.Form):
    captcha = CaptchaField()  # 验证码字段
