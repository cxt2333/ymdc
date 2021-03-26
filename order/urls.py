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

from order import views

app_name = 'order'
urlpatterns = [
    # 订单管理
    path('order/', views.OrderListView.as_view(), name='order'),
    path('order/<int:status>/', views.OrderListView.as_view(), name='order'),
    path('order/<int:status>/<int:page>/', views.OrderListView.as_view(), name='order'),
    # 订单添加
    path('addorder/', views.AddOrderView.as_view(), name='addOrder'),
    # 订单支付
    path('payorder/', views.PayOrderView.as_view(), name='payOrder'),
]
