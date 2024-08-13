from django.urls import path
from .views import OrderCreateView,OrderListView,OrderDetailView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('list/', OrderListView.as_view(), name='order_list'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]