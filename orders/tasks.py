from django.core.mail import send_mail
from .models import Order
import dramatiq

@dramatiq.actor
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
            f'You have successfully placed an order.' \
            f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                        message,
                        'admin@myshop.com',
                        [order.email],
                        fail_silently=False)
    print("inside task")
    return mail_sent
