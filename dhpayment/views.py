import os
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from dhpayment.models import Patient, Interv
import stripe
import qrcode
import qrcode.image.svg
from io import BytesIO
from stripeProject import settings

stripe.api_key = settings.STRIPE_API_KEY


def index(request):
    return None


class IntervListView(ListView):
    model = Interv
    paginate_by = 100


def create_checkout_session(request, pk):
    interv = get_object_or_404(Interv, pk=pk)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'locale': 'fr',
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
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
    )

    return redirect(session.url, code=303)


def createQrCode(request, uuid):
    context = {}
    interv = get_object_or_404(Interv, uuid=uuid)
    text = 'http://127.0.0.1:8000/card/' + interv.uuid
    img = qrcode.make(text)
    img.save(interv.uuid + ".png")
    context["img"] = img
    return render(request, "dhpayment/interv_list.html", context=context)
