from django.shortcuts import render, get_object_or_404
from .models import Order


def thanks(request, order_id):
    '''
    기능 : 주문 완료 후에 thanks.html 템플릿으로 redirect('order:thanks', order_details.id)

    '''
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
        return render(request, 'thanks.html', {'customer_order': customer_order})
