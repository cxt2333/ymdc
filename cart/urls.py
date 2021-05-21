"""ymdc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from cart import views

app_name = 'cart'
urlpatterns = [
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('addcart/', views.AddCartView.as_view(), name='addCart'),
    # 购物车数量修改
    path('changecartnum/<int:cid>/<int:num>/', views.ChangeCartNumView.as_view(), name='changeCartNum'),
    # 购物车删除
    path('delcart/<int:cid>/', views.DelCartView.as_view(), name='delCart'),
]
