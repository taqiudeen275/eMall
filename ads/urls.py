# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get-popup-ad/', views.get_popup_ad, name='get_popup_ad'),
    path('record-ad-click/<int:ad_id>/', views.record_ad_click, name='record_ad_click'),
]