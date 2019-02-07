from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product
from .models import Cart, CartItem


def _cart_id(request):
    """
    기능: CartItem 의 필드로 장바구니를 식별하기 위해 사용

    설명: str 타입의 32글자로 세션키를 받아서 처리
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """
    기능: 장바구니(cart) 에 담아 cart.html(장바구니 페이지)에 렌더링

    설명:
    1. product_id 로 특정 상품을 구분(objects.get)
    2. Cart 모델의 필드를 생성(또는 objects.get)
    3. CartItem 모델의 필드를 생성(또는 objects.get) (조건) 해당 Product.stock 이 재고에 있을 때만 추가

    """
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    """
    기능: 담겨져 있는 장바구니에 대한 합산 가격, 각 상품에 수량 등을 리턴하는 기능

    :param total: 장바구니의 총 합산 가격
    :param counter: 장바구니 안에서 각 상품에 대한 구매 예정 수량
    :param cart_items: cart_id 에 해당하는 아이템들
    """
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    return render(request, 'cart/cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def remove_cart(request, product_id):
    """
    기능: 장바구니 안에 담겨져 있는 특정 상품의 수량을 삭제

    설명: CartItem 에서 filter(쿼리셋) 가 아닌 get(객체) 을 사용하여 for loop 를 사용하지 않고 특정 객체에 대한 처리
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, product_id):
    """
    기능: 장바구니 안에 담겨져 있는 상품 자체를 삭제

    설명: Product 모델에서 해당하는 product_id 가 있으면 장바구니(CartItem) 에서 delete()
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
