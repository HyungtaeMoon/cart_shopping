from django.contrib import admin

from .models import Order, OrderItem


# 모델 필드를 옆으로 펼치는 방식(TabularInline)
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'], }),
        ('Quantity', {'fields': ['quantity'], }),
        ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    # 구매한 아이템에 대해서 삭제 기능
    can_delete = False
    # 저장 가능한 최대 항목 개수
    max_num = 0
    template = 'admin/order/tabular.html'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billingName', 'emailAddress', 'created_at']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'emailAddress']
    # 나중에 DB 가 많아져서 주문 내역을 보는데까지 오래 걸릴 경우 + 주문자에 대한 정보를 수정할 필요가 없는 경우, readonly_fields 를 권장
    readonly_fields = ['id', 'token', 'total', 'emailAddress', 'created_at', 'billingName', 'billingAddress1',
                       'billingCity', 'billingPostcode', 'billingCountry', 'shippingName', 'shippingAddress1',
                       'shippingCity', 'shippingPostcode', 'shippingCountry']
    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'created_at']}),
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1', 'billingCity',
                                            'billingPostcode', 'billingCountry', 'emailAddress']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1', 'shippingCity',
                                             'shippingPostcode', 'shippingCountry']})
    ]

    # Order --(FK)-> OrderItem 관계에 inlines 를 사용
    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
