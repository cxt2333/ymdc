from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from user.models import Cart, Foods


class CartListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'user/login.html', {'msg': '您尚未登录，请登录后访问购物车'})
        carts = Cart.objects.filter(user_id=request.user.uid, c_is_select=1)
        allprice = self.compute(carts)
        return render(request, 'cart/cart.html', locals())

    # 计算购物中用户所选商品总价
    def compute(self, carts):
        # 计算总价
        total = 0
        for rec in carts:
            total += rec.c_food_num * rec.food_id.food_price
        return total


class AddCartView(View):
    def post(self, request, *args, **kwargs):
        # 获取商品id
        food_id = request.POST.get('id')
        food_num = request.POST.get('foodNum')
        print(food_num, type(food_num))
        # 获取商品
        food = Foods.objects.get(pk=food_id)
        # 获取用户
        user = request.user
        # 购物车查询当前用户购物车记录
        carts = Cart.objects.filter(user_id=user, c_is_select=1)
        # 查询该用户购物车是否有相同商品
        carts = carts.filter(food_id=food)
        # 判断是否有该商品
        if carts.exists():
            # 存在该商品，数量加1
            cart = carts.first()
            cart.c_food_num += int(food_num)
            cart.save()
        else:
            # 没有该商品，添加该商品
            cart = Cart()
            cart.c_food_num = 1
            cart.c_is_select = 1
            cart.food_id = food
            cart.user_id = user
            cart.save()
        return JsonResponse({'msg': '加入购物车成功'})
