from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .forms import BusinessRegistrationForm, BusinessUpdateForm
from .models import Business
from django.views.generic import TemplateView


class BusinessRegistrationView(LoginRequiredMixin, CreateView):
    model = Business
    form_class = BusinessRegistrationForm
    template_name = 'business/register.html'
    success_url = reverse_lazy('business_registration_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class BusinessRegistrationSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'business/business_registration_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = self.request.user.business
        return context
    

class BusinessUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Business
    form_class = BusinessUpdateForm
    template_name = 'business/update.html'
    success_url = reverse_lazy('business_detail')  # Or wherever you want to redirect after successful update

    def test_func(self):
        # Ensure that only the owner of the business can update it
        business = self.get_object()
        return self.request.user == business.user

    def get_object(self, queryset=None):
        # Get the business object for the current user
        return self.request.user.business

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed
        # It should return an HttpResponse
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class BusinessDetailView(LoginRequiredMixin, DetailView):
    model = Business
    template_name = 'business/detail.html'
    context_object_name = 'business'

    def get_object(self, queryset=None):
        return self.request.user.business

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class PublicBusinessProfileView(DetailView):
    model = Business
    template_name = 'business/public_business_profile.html'
    context_object_name = 'business'

    def get_object(self, queryset=None):
        return get_object_or_404(Business, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.filter(available=True).order_by('-created_at')
        return context