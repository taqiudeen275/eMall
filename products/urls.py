from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('dashboard/product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
     path('product/add/', views.ProductCreateView.as_view(), name='product_add'),
]