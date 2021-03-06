from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from user.models import Type, Foods
from home.tools import BaiduPaginator


def index(request):
    # 在后端判断是否登入，前者为用者为户名，后身份验证放回布尔值
    print(request.user, request.user.is_authenticated)
    return render(request, 'templates/user/info.html')


class HomeView(View):
    def get(self, request, tid=0, page=1):
        foodtypes = Type.objects.all()
        # 获取所有分类id
        postion = [ft.tid for ft in foodtypes]
        pos = postion.index(tid)
        if tid == 0:
            foods = Foods.objects.all()
        else:
            # food检索
            foods = Foods.objects.filter(type_id=tid)

        paginator = BaiduPaginator(foods, 3)
        pager = paginator.page(page)
        pager.page_range = paginator.custom_range(paginator.num_pages, page, 3)
        return render(request, 'home/home.html', locals())

    def post(self, request, *args, **kwargs):
        foodtypes = Type.objects.all()
        # 获取所有分类id
        postion = [ft.tid for ft in foodtypes]

        tid = int(request.POST.get('tid', 0))
        keyword = request.POST.get('keyword', '')

        # 食品检索
        foods = Foods.objects.filter(food_name__icontains=keyword)

        # pos = postion.index(tid)
        # if tid == 0:
        #     foods = food.all()
        # else:
        #     # food检索
        #     foods = food.filter(type_id=tid)
        page = 1
        paginator = BaiduPaginator(foods, 3)
        pager = paginator.page(page)
        pager.page_range = paginator.custom_range(paginator.num_pages, page, 3)
        return render(request, 'home/home.html', locals())
