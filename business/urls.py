from django.urls import path
from .views import BusinessRegistrationSuccessView,BusinessRegistrationView,BusinessUpdateView,BusinessDetailView,PublicBusinessProfileView



urlpatterns = [
    path('registration/', BusinessRegistrationView.as_view(), name='business_registration'),
    path('registration/success/', BusinessRegistrationSuccessView.as_view(), name='business_registration_success'),
    path('business/update/', BusinessUpdateView.as_view(), name='business_update'),
    path('business/profile/', BusinessDetailView.as_view(), name='business_detail'),
    path('business/<int:pk>/', PublicBusinessProfileView.as_view(), name='public_business_profile'),
]
