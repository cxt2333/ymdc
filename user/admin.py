from django.contrib import admin

# Register your models here.
from user.models import User, Foods, Type, Cart, Order, Orderfoods


class UserAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['uid', 'username', 'password', 'email', 'phone', 'sex', 'is_active']
    # 搜索字段
    search_fields = ['username']
    # 分页
    list_per_page = 5


class FoodsAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['fid', 'food_name', 'food_price', 'food_describe', 'sell_num', 'food_img', 'type_id']
    # 搜索字段
    search_fields = ['food_name']
    # 分页
    list_per_page = 5


class TypeAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['tid', 'type_name']
    # 搜索字段
    search_fields = ['type_name']
    # 分页
    list_per_page = 5


class CartAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['cid', 'c_food_num', 'c_is_select', 'food_id', 'user_id']
    # 搜索字段
    # search_fields = ['user_name']
    # 分页
    list_per_page = 5


class OrderAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['oid', 'o_price', 'o_time', 'o_status', 'user_id']
    # # 搜索字段
    # search_fields = ['food_name']
    # 分页
    list_per_page = 5


class OrderFoodsAdmin(admin.ModelAdmin):
    # 显示字段
    list_display = ['ofid', 'of_food_num', 'food_id', 'order_id']
    # # 搜索字段
    # search_fields = ['food_name']
    # 分页
    list_per_page = 5


admin.site.register(User, UserAdmin)
admin.site.register(Foods, FoodsAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Orderfoods,OrderFoodsAdmin)
