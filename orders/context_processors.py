from orders.models import Order

def order_items(request):
    data = {
        'order_items': Order.objects.get(customer=request.user).get_order_items(),
    }
    return data
