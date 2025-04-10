from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from bdenapp.models import Property
from django.shortcuts import get_object_or_404


# Create your views here.

def initiate_payment(request, property_id):
    if request.method == "POST":
        user = request.user
        property = get_object_or_404(Property, id=property_id)
        amount = property.price
        email = user.email
        

        if not amount or not email:
            return HttpResponse("Missing required payment details", status=400)

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        return redirect('payments:payment_confirmation', payment_id=payment.id)
    return HttpResponse("Invalid request", status=400)

# payment confirmation
def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount_value': payment.amount_value(),
        'property': payment.user.profile.property if hasattr(payment.user.profile, 'property') else None,
    }
    return render(request, 'payments/make_payment.html', context)

def verify_payment(request, ref, property_id):
    print("Received ref:", ref)
    print("Received property_id:", property_id)
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()

    if verified:
        user_wallet = UserWallet.objects.get(user=request.user)
        user_wallet.balance = payment.amount
        user_wallet.save()
        property_obj = get_object_or_404(Property, id=property_id)
        
        receipt_data = {
            'user' : request.user.username,
            'email' : request.user.email,
            'amount': payment.amount,
            'reference': payment.ref,
            'date': payment.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'wallet_balance': user_wallet.balance,
            'property_name': property_obj.description,
            'property_price': property_obj.price,
            'property_location': getattr(property_obj, 'location', 'Not specified'),  
        }
        return render(request, "payments/success.html", {'receipt': receipt_data, 'wallet_balance': user_wallet.balance})
    return render(request, "payments/success.html", {'error': "Payment verification failed."})
