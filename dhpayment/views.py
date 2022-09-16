from pprint import pprint

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from dhpayment.models import Interv
import stripe
import qrcode
from stripeProject import settings

stripe.api_key = settings.STRIPE_API_KEY
endpoint_secret = settings.ENDPOINT_SECRET


def index(request):
    return None


class IntervListView(ListView):
    model = Interv
    paginate_by = 100


def create_checkout_session(request, uuid):
    interv = get_object_or_404(Interv, uuid=uuid)
    session = stripe.checkout.Session.create(
        client_reference_id=interv.uuid,
        customer_email=interv.patient.email,
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': "Honoraires d'anesthésie",
                },
                'unit_amount': interv.amount * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('checkout-success')),
        cancel_url=settings.SERVER_IP + '/card/cancel',
    )

    return redirect(session.url, code=303)


def createQrCode(request, uuid):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    pathqr = settings.QR_CODE
    interv = get_object_or_404(Interv, uuid=uuid)
    text = 'http://liveproject.ddns.net/card/create-checkout-session/' + interv.uuid
    data = qr.add_data(text)
    img = qr.make_image(data)
    imgqrcode = interv.uuid + ".png"
    imgpath = str(pathqr) + "/" + imgqrcode
    img.save(imgpath)
    return HttpResponse(f'<div class="mt-5"><img src="/static/media/qrcode/{imgqrcode}" width="300" length="300"></div>'
                        f'<div class="ml-4">{interv.patient} {interv.amount} €</div>')


def checkout_success(request):
    return render(request, 'dhpayment/result/success.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        uuid = event['data']['object']['client_reference_id']
        interv = get_object_or_404(Interv, uuid=uuid)
        interv.payment_state = 'PAY'
        interv.save()
        return HttpResponse(status=200)

    return HttpResponse(status=200)


def state_pay(request):
    status = Interv.objects.all()
    for stat in status:
        stat.payment_state = 'ATT'
        stat.save()
    return render(request, 'dhpayment/interv_list.html')
