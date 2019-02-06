from django.shortcuts import render

from django.db.models import Q
from shop.models import Product


def search_result(request):
    """
    검색 상품에 대한 결과를 보여주는 기능

    1) input 에서 받은 name=q 를 키워드로,
    2) Q 모델을 활용하여 Product 에 대한 상품명, 설명에 대한 필터링 값을 products 에 담아 렌더링

    :return: query, products
    """
    products = None
    query = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
        # query 를 렌더에 굳이 포함시킨 이유는 search.html 에서 {{ query }} 에서 검색어를 보여주기 위함
        return render(request, 'search_app/search.html', {'query': query, 'products': products})
