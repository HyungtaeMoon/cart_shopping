from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    """
    기능: 장바구니에 몇개를 담았는지에 대한 정보를 보여줌
    - My cart(4): 총 수량 4개의 아이템이 담겨져 있음

    설명: view 에서 처리하면 render 로 item_count 에 대한 정보를 뿌려줘야 하지만
    settings/TEMPLATES/OPTIONS/context_processors 에 정의해두어 리턴 값을 템플릿에서 바로 사용 가능 {{ item_count }}
    """
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
                print(f'각각의 아이템을 순회하며 item_count 에 + 1 [추가(조회)상품]({cart_item.product}:{cart_item.quantity})')
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)
