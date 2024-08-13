from django.views.generic import CreateView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import Cart
from django.shortcuts import get_object_or_404


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('order_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user).items.all()
        total = sum(item.product.price * item.quantity for item in cart)
        context['cart'] = cart
        context['total'] = total
        return context

    def form_valid(self, form):
        
        cart = get_object_or_404(Cart, user=self.request.user).items.all()
        total = sum(item.product.price * item.quantity for item in cart)
        if not cart:
            messages.error(self.request, "Your cart is empty.")
            return redirect('cart_detail')

        order = form.save(commit=False)
        order.user = self.request.user
        order.total_amount = total
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            # Reduce stock
            item.product.reduce_stock(item.quantity)

        # Clear the cart
        cart.delete()

        messages.success(self.request, "Your order has been placed successfully.")
        return super().form_valid(form)
    



class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')



class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)