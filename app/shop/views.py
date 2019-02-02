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
    products = None
    # category 의 slugField 가 None 이 아닌 경우에
    if c_slug!=None:
        # Product 객체를 만들고, url 을 통해 들어온 slug 필드를 Category.slugField 에 매핑
        c_page = get_object_or_404(Category, slug=c_slug)
        # DB 에 접근(조건은 c_page: 상품에 해당하는 모든 카테고리, available 이 True 값)
        products = Product.objects.filter(category=c_page, available=True)
    else:
        # c_slug 가 None: url 에서 slug 를 입력하지 않고 접근할 경우,
        #  available 가 True 인 모든 상품 페이지를 보여줌
        products = Product.objects.all().filter(available=True)
    # context 에 c_page 가 있으면 category 와 매핑하여 보여주고
    #   없으면 이용가능한 모든 상품을 렌더 시켜줌
    return render(request, 'shop/category.html', {'category': c_page, 'products': products})


def product_cat_detail(request, c_slug, product_slug):
    try:
        # Category 에 해당하는 Product 객체만 보여줘야 하기 때문에 아래의 2가지 조건에 맞는 객체들만 할당
        #   1. Category <-- Product (FK) 에 의해 category__slug 로 접근하여 c_slug 매칭
        #   2. Product.objects.get(slug=product_slug) 를 매칭
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product-detail.html', {'product': product})
