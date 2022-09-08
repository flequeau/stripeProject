from django.urls import path
from dhpayment import views

urlpatterns = [
    path('', views.IntervListView.as_view(), name='interv-list'),
    path('card/create-checkout-session', views.create_checkout_session, name='create-check-out-session'),
    path('card/<str:uuid>', views.createQrCode, name='create-qrcode'),
]