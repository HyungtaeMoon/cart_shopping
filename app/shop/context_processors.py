from .models import Category


def menu_links(request):
    # QuerySet 을 links 변수에 할당
    links = Category.objects.all()
    # dict 타입으로 형변환을 하면 아래와 같이 return 되어 'links':<Queryset> 의 형태를 가짐
    # {'links': <QuerySet [<Category: Cotton Cushions>, <Category: Polyester Cushion>]>}
    return dict(links=links)
