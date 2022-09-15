from django.urls import path
from dhpayment import views

urlpatterns = [
    path('', views.IntervListView.as_view(), name='interv-list'),
    path('card/create-checkout-session/<str:uuid>', views.create_checkout_session, name='create-check-out-session'),
    path('card/qr/<str:uuid>', views.createQrCode, name='create-qrcode'),
    path('card/success', views.checkout_success, name='checkout-success'),
    path('card/status', views.state_pay, name='status'),
    path('webhook', views.stripe_webhook, name='stripe-webhook')
]
