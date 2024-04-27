from io import BytesIO
import dramatiq
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@dramatiq.actor
def payment_completed(order_id):
    '''
    Task to send e-mail notifications when an order is paid
    '''

    order = Order.objects.get(id=order_id)
    #create invoice e-mail
    subject = f'My shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    #generate pdf
    html = render_to_string('orders/order/pdf.html',{'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)

    #attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    
    email.send()