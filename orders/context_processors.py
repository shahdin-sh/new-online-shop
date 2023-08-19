from orders.models import Order


def order_items(request):
    data = {}
    user = request.user
    if user.is_authenticated and user.order:
        data = {
            'order_items': user.order.get_order_items()
        }
    return data
