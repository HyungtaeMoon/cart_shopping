from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def index(request):
    text_var = 'hello this is index page'
    return HttpResponse(text_var)


def allProdCat(request, c_slug=None):
    """
    allProdCat 에 2가지 경우에 대한 return
    1. url 에서 slug 필드(cotton-cushions) 로 접근하면 해당 slug 필드의 값들을 보여줌
    2. 그게 아닌 경우에는 모든 상품 페이지를 보여줌
    """
    # category 페이지
    c_page = None
    products_list = None

    # category 의 slugField 가 None 이 아닌 경우에
    if c_slug!=None:
        # Product 객체에 접근하고, url 을 통해 들어온 slug 필드를 Category.slugField 에 매핑
        c_page = get_object_or_404(Category, slug=c_slug)
        # DB 에 접근(조건은 c_page: 상품에 해당하는 모든 카테고리, available 이 True 값)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        # c_slug 가 None: url 에서 slug 를 입력하지 않고 접근할 경우,
        #  available 가 True 인 모든 상품 페이지를 보여줌
        products_list = Product.objects.all().filter(available=True)

    # Paginator(object_list, per_page)
    paginator = Paginator(products_list, 6)
    try:
        # paginator 로 몇번째의 페이지로 get 요청을 최초로 보낼지 설정
        #   ('2'로 설정하면 최초 get 요청으로 보여지는 페이지는 2페이지로 설정됨)
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        # 위의 try, except 문에서 설정한 page 변수를 사용하여 products 의 페이지 설정
        #   paginator.page 에서 page 는 Paginator 의 메서드, (page) 는 위에서 변수로 지정한 page
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        print(f'?page={page} 는 존재하지 않는 페이지로 2페이지에서 url get 요청 또는 str 입력시 2페이지로 다시 redirect 됩니다')
        products = paginator.page(paginator.num_pages)

    # context 에 c_page 가 있으면 category 와 매핑하여 보여주고
    #   없으면 이용가능한 모든 상품을 렌더 시켜줌
    return render(request, 'shop/category.html', {'category': c_slug, 'products': products})


def product_cat_detail(request, c_slug, product_slug):
    try:
        # Category 에 해당하는 Product 객체만 보여줘야 하기 때문에 아래의 2가지 조건에 맞는 객체들만 할당
        #   1. Category <-- Product (FK) 에 의해 category__slug 로 접근하여 c_slug 매칭
        #   2. Product.objects.get(slug=product_slug) 를 매칭
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product-detail.html', {'product': product})
