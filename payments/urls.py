from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate-payment/<int:property_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment-confirmation/<int:payment_id>/<int:property_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('verify-payment/<str:ref>/<int:property_id>/', views.verify_payment, name='verify_payment'),
]
