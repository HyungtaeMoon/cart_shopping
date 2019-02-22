from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem


def thanks(request, order_id):
    '''
    기능 : 주문 완료 후에 thanks.html 템플릿으로 redirect('order:thanks', order_details.id)

    '''
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
        return render(request, 'thanks.html', {'customer_order': customer_order})


@login_required
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(emailAddress=email)
        context = {
            'order_details': order_details,
        }
    return render(request, 'order/orders_list.html', context)


@login_required
def view_order(request, order_id):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order = Order.objects.get(id=order_id, emailAddress=email)
        order_items = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'order_items': order_items,
        }
    return render(request, 'order/order_detail.html', context)
