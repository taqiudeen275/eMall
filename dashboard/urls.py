# In your ads/urls.py file

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ad/create/', views.create_ad, name='ad_create'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:pk>/update/', views.ad_update, name='ad_update'),
    path('ads/', views.ad_list, name='ad_list'),

    path('products/', views.DashboardProductListView.as_view(), name='dashboard_product_list'),
    path('products/<int:pk>/edit/', views.ProductEditView.as_view(), name='dashboard_product_edit'),
    path('products/<int:pk>/', views.DashboardProductDetailView.as_view(), name='dashboard_product_detail'),

    path('orders/', views.DashboardOrderListView.as_view(), name='dashboard_order_list'),
    path('orders/<int:pk>/', views.DashboardOrderDetailView.as_view(), name='dashboard_order_detail'),
    path('orders/<int:pk>/update-status/', views.DashboardOrderUpdateStatusView.as_view(), name='dashboard_order_update_status'),
    
]