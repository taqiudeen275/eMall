from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Sum, Count
from django.urls import reverse_lazy
from business.models import Business
from orders.models import Order, OrderItem
from products.forms import ProductForm
from products.models import Product, ProductImage
from .models import Ad
from .forms import AdForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,UpdateView,DetailView


@login_required
def dashboard(request):

    my_products = Product.objects.filter(business=request.user.business)
    context = {
        'total_products': Product.objects.filter(business=request.user.business).count(),
        'total_sales': my_products.annotate(order_count=Count('order_items')).aggregate(total_orders=Sum('order_count'))['total_orders'] or 0,
        'active_ads': Ad.objects.filter(is_active=True,created_by=request.user.business).count(),
        'recent_products': Product.objects.filter(business=request.user.business).order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/index.html', context)


def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.created_by = request.user.business  # Assuming the user has an associated business
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'dashboard/create_ad.html', {'form': form})



def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'dashboard/ad_details.html', {'ad': ad})

@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    
    # Check if the user has permission to edit this ad
    if ad.created_by != request.user.business:
        return redirect('ad_detail', pk=ad.pk)
    
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    
    return render(request, 'dashboard/ad_update.html', {'form': form, 'ad': ad})


def ad_list(request):
    ads = Ad.objects.filter(created_by=request.user.business).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(ads, 10)  # Show 10 ads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/ad_list.html', {'page_obj': page_obj})





class DashboardProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'dashboard/products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        business = get_object_or_404(Business, user=self.request.user)
        return Product.objects.filter(business=business).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        business = get_object_or_404(Business, user=self.request.user)
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id, business=business)

        if action == 'toggle_featured':
            product.featured = not product.featured
            product.save()
        elif action == 'delete':
            product.delete()

        return redirect('dashboard_product_list')
    
class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/product_update.html'
    success_url = reverse_lazy('dashboard_product_list')

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('pk')
        business = get_object_or_404(Business, user=self.request.user)
        return get_object_or_404(Product, id=product_id, business=business)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['primary_image'].required = False
        return form

    def get_initial(self):
        initial = super().get_initial()
        primary_image = self.object.images.filter(is_primary=True).first()
        if primary_image:
            initial['primary_image'] = primary_image.image
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get('primary_image'):
            ProductImage.objects.filter(product=self.object, is_primary=True).delete()
            ProductImage.objects.create(product=self.object, image=form.cleaned_data['primary_image'], is_primary=True)
        if form.cleaned_data.get('additional_images'):
            ProductImage.objects.filter(product=self.object, is_primary=False).delete()
            for image in form.cleaned_data['additional_images']:
                ProductImage.objects.create(product=self.object, image=image)
        return response
    

class DashboardProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'dashboard/product_details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('pk')
        business = get_object_or_404(Business, user=self.request.user)
        return get_object_or_404(Product, id=product_id, business=business)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Add additional context data here
        context['total_sales'] = product.order_items.count()  # Assuming you have a related name 'order_items' in your Order model
        context['revenue'] = sum(item.price * item.quantity for item in product.order_items.all())
        context['in_stock'] = product.stock > 0
        context['low_stock'] = product.stock < 10  # Adjust this threshold as needed
        
        return context
    


class BusinessRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'business')

class DashboardOrderListView(LoginRequiredMixin, BusinessRequiredMixin, ListView):
    model = Order
    template_name = 'dashboard/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        business = self.request.user.business
        return Order.objects.filter(items__product__business=business).distinct().order_by('-created_at')

class DashboardOrderDetailView(LoginRequiredMixin, BusinessRequiredMixin, DetailView):
    model = Order
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        business = self.request.user.business
        return Order.objects.filter(items__product__business=business).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.request.user.business
        context['order_items'] = OrderItem.objects.filter(order=self.object, product__business=business)
        return context
    


class DashboardOrderUpdateStatusView(LoginRequiredMixin, BusinessRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/dashboard_order_update_status.html'

    def get_success_url(self):
        return reverse_lazy('dashboard_order_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        business = self.request.user.business
        return Order.objects.filter(items__product__business=business).distinct()