from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from features.models import Feature
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Sum, F
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView

def _get_open_order(request):
    if request.user.is_authenticated:
        order, _ = Order.objects.get_or_create(
            user=request.user, checked_out=False)
    else:
        order_id = request.session.get('order_id')
        order = Order.objects.filter(
            id=order_id, checked_out=False).first() if order_id else None
        if not order:
            order = Order.objects.create()
            request.session['order_id'] = order.id
    return order

class AddToCartView(View):
    def get(self, request, pk):
        feature = get_object_or_404(Feature, pk=pk)
        order = _get_open_order(request)
        item, created = OrderItem.objects.get_or_create(
            order=order, feature=feature,
            defaults={'price': feature.size * 0.1}
        )
        if not created:
            item.quantity += 1
            item.save()
        return redirect('orders:cart')

class CartView(View):
    def get(self, request):
        order = _get_open_order(request)
        items = order.items.all() if order else []
        return render(request, 'orders/cart.html',
                      {'order': order, 'items': items})

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        order = _get_open_order(request)
        order.user = request.user
        order.checked_out = True
        order.save()
        request.session.pop('order_id', None)
        return render(request, 'orders/checkout_success.html',
                      {'order': order})

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user,
            checked_out=True
        ).order_by('-created')

@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'orders/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = (
            OrderItem.objects
            .filter(order__checked_out=True)
            .values('feature__feature_type')
            .annotate(total_sales=Sum(F('price') * F('quantity')))
            .order_by('-total_sales')
        )
        context['labels'] = [row['feature__feature_type'] for row in qs]
        context['data']   = [float(row['total_sales']) for row in qs]
        return context
