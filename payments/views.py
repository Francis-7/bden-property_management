from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from bdenapp.models import Property
from django.shortcuts import get_object_or_404
import os
from reportlab.pdfgen import canvas


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

        return redirect('payments:payment_confirmation', payment_id=payment.id, property_id=property.id)
    return HttpResponse("Invalid request", status=400)

# payment confirmation
def payment_confirmation(request, payment_id, property_id):
    payment = get_object_or_404(Payment, id=payment_id)
    property_obj = get_object_or_404(Property, id=property_id)
    
    context = {
        'payment': payment,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount_value': payment.amount_value(),
        'property': property_obj,
    }
    return render(request, 'payments/make_payment.html', context)

def verify_payment(request, ref, property_id):
    
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    property = get_object_or_404(Property, id=property_id)

    if verified:
        user_wallet = UserWallet.objects.get(user=request.user)
        user_wallet.balance = payment.amount
        user_wallet.save()
        property_obj = get_object_or_404(Property, id=property_id)
        print("Property ID in view:", property_obj.id)
        
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
        response = render(request, "payments/success.html", {'receipt': receipt_data, 'wallet_balance': user_wallet.balance, 'property':property})

        pdf_filename = f"receipt_{payment.ref}.pdf"
        pdf_filepath = os.path.join("media/receipts", pdf_filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(pdf_filepath), exist_ok=True)
        
        c = canvas.Canvas(pdf_filepath)
        c.setFont("Helvetica", 12)

        y_position = 800
        c.drawString(100, y_position, "Payment Receipt")
        y_position -= 40
        
        for key, value in receipt_data.items():
            c.drawString(100, y_position, f"{key}: {value}")
            y_position -= 20
        
        c.save()

        payment.receipt_pdf = pdf_filename
        payment.save()

        return response
    return render(request, "payments/success.html", {'error': "Payment verification failed."})
