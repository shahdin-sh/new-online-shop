from orders.models import Order


def order_items(request):
    data = {}
    # user = request.user
    # user_order = Order.objects.filter(customer=user).exists()
    # if user.is_authenticated and user_order:
    #     data = {
    #         'order_items': user.order.get_order_items()
    #     }
    return data
