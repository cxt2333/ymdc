from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from home.tools import BaiduPaginator
from user.models import Order, Orderfoods, Cart
from ymdc import settings


class OrderListView(View):
    def get(self, request, status=-1, page=1):
        if not request.user.is_authenticated:
            return render(request, 'user/login.html', {'msg': '您尚未登录，请登录后访问订单'})
        if status < 0:
            orders = Order.objects.filter(user_id=request.user.uid)
        else:
            orders = Order.objects.filter(user_id=request.user.uid).filter(o_status=status)

        pos = status + 1

        orderfoods = Orderfoods.objects.all()

        paginator = BaiduPaginator(orders, 2)
        pager = paginator.page(page)
        pager.page_range = paginator.custom_range(paginator.num_pages, page, 3)
        return render(request, 'order/order.html', locals())


class AddOrderView(View):
    def get(self, request, *args, **kwargs):
        # 找到用户在购物车中所选商品
        carts = Cart.objects.filter(user_id=request.user).filter(c_is_select=1)
        # 创建订单
        my_order = Order()
        my_order.o_price = self.compute(carts)
        my_order.o_status = settings.ORDER_STATUS_NOT_PAY
        my_order.user_id = request.user
        my_order.save()

        # 购物车商品添加到订单商品表
        self.add_to_orderfoods(my_order, carts)
        return render(request, 'order/order.html')

    # 计算购物中用户所选商品总价
    def compute(self, carts):
        # 计算总价
        total = 0
        for rec in carts:
            total += rec.c_food_num * rec.food_id.food_price
        return total

    def add_to_orderfoods(self, my_order, carts):
        # 创建多个对象
        res = []
        for cart in carts:
            # 实例化订单商品对象
            order_foods = Orderfoods()
            order_foods.of_food_num = cart.c_food_num
            order_foods.food_id = cart.food_id
            order_foods.order_id = my_order
            res.append(order_foods)
        Orderfoods.objects.bulk_create(res)


class PayOrderView(View):
    def post(self, request, *args, **kwargs):
        # 获取订单id与状态
        order_id = request.POST.get('oid')
        status = request.POST.get('status')
        print(order_id, status)
        return JsonResponse({'msg': '支付成功'})
