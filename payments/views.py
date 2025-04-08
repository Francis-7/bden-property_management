from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings
from django.http import JsonResponse, HttpResponse

# Create your views here.

def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']

        if not amount or not email:
            return HttpResponse("Missing required payment details", status=400)

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
        }
        return render(request, 'payments/make_payment.html', context)
    template_name = request.GET.get('template', 'payment')
    return render(request, 'payments/payment.html')

def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        user_wallet = UserWallet.objects.get(user=request.user)
        user_wallet.balance += payment.amount
        user_wallet.save()
        print(request.user.username, " funded wallet successfully")
        return render(request, "payments/success.html")
    return render(request, "payments/success.html")
