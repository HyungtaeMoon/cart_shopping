from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('thanks/<int:order_id>/', views.thanks, name='thanks'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.view_order, name='order_detail'),
]
