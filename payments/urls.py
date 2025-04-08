from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
]
