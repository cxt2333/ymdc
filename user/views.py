from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.generic.base import View

from user.form import RegisterForm, ChangeForm

# Create your views here.
from user.models import User
from user.util import token_confirm
from ymdc.settings import EMAIL_FROM


class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'templates/user/register.html')

    def post(self, request, *args, **kwargs):
        # 用提交的数据生成表单
        form = RegisterForm(request.POST)
        # 能通过验证，返回True，否则放回False
        if form.is_valid():
            # 进行业务处理
            data = form.cleaned_data
            # 删除确认密码
            data.pop('confirm')
            # 把用户写入数据库
            # 密码回自动做一个签名加密，不能手动签名加密password
            user = User.objects.create_user(**data)
            if user:
                # 发送邮箱，确认激活
                token = token_confirm.generate_validate_token(user.pk)
                print(token)
                # 构建验证url
                url = 'http://' + request.get_host() + reverse('user:active', kwargs={'token': token})
                # 加载模块
                html = loader.get_template('user/active.html').render({'url': url})
                print(url)
                send_mail('账号激活', '', EMAIL_FROM, [user.email], html_message=html)
                return HttpResponse('激活邮件已发送，请登录邮箱确认激活,完成账号注册')
            else:
                return render(request, 'templates/user/register.html', {'form': form})
        else:
            # 验证不成功，把错误信息渲染到前端界面
            return render(request, 'templates/user/register.html', {'form': form})


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'templates/user/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user_active = User.objects.get(username=username)
        except:
            return render(request, 'user/login.html', {'msg': '用户名或密码错误'})
        if not user_active.is_active:
            return render(request, 'user/login.html', {'msg': '账号未激活，请查看注册邮箱激活账号'})
        # 用户验证，如果用户名和密码真确，放回User对象，否则放回None
        user = authenticate(request, username=username, password=password)
        if user:
            # 记录用户登录状态，参数是请求对象和用户对象
            login(request, user)
            return redirect(reverse('home:home'))
        else:
            return render(request, 'user/login.html', {'msg': '用户名或密码错误'})


def user_logout(request):
    logout(request)
    return redirect(reverse('user:login'))


def active_user(request, token):
    try:
        uid = token_confirm.confirm_validate_token(token)
    except:
        try:
            uid = token_confirm.remove_validate_token(token)
            user = User.objects.get(pk=uid)
            user.delete()
        except:
            return HttpResponse('激活失败，请重新注册用户')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse('你激活的用户不存在，请重新注册')
    user.is_active = 1  # 激活用户
    user.save()
    # 删除token
    token_confirm.remove_validate_token(token)
    return render(request, 'user/login.html', {'msg': '用户已激活，请登录系统'})


@login_required(login_url='/user/login/')
def userInfo(request):
    username = request.user.username
    email = request.user.email
    phone = request.user.phone
    if request.user.sex:
        sex = '男'
    else:
        sex = '女'
    return render(request, 'user/info.html', locals())


class changeUserInfo(View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        email = request.user.email
        phone = request.user.phone
        sex = request.user.sex
        return render(request, 'user/changeInfo.html', locals())

    def post(self, request, *args, **kwargs):
        form = ChangeForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = User.objects.filter(pk=request.user.uid)
            user.update(**form.cleaned_data)
            return redirect(reverse('user:info'))
        else:
            # 验证不成功，把错误信息渲染到前端界面
            return render(request, 'user/changeInfo.html', {'form': form})
