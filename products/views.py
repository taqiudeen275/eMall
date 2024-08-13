from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from products.forms import ProductForm
from .models import Product, Category
from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort = self.request.GET.get('sort', 'name')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('name')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get related products (same category, excluding current product)
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        
        context['related_products'] = related_products
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.business = self.request.user.business 
        
        return super().form_valid(form)
    


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['category', 'name', 'description', 'price', 'stock', 'available']
    success_url = reverse_lazy('product_list')



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')



def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'products/category_products.html', {'category': category, 'products': products})


def home(request):
    categories = Category.objects.all()[:3]
    featured_products = Product.objects.filter(featured=True)[:4]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)