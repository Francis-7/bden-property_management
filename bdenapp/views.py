from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, PropertyImage, Review, UserProfile, User, SavedItems, Purchase
from .filters import PropertyFilter
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, PropertyForm, PropertyImageForm, ReviewForm, UserProfileForm
from .models import group_and_sort_by_first_word
from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import Counter
import requests
from django.conf import settings


def home_view(request):
    properties = Property.objects.all().order_by('location')
    grouped_data = group_and_sort_by_first_word()
    return render(request, 'bdenapp/home.html', {'properties': properties, 'groups' : grouped_data})

def propertyView(request, id):
    property = get_object_or_404(Property, id=id)
    images = property.propertyimage_set.all()
    properties = Property.objects.all()
    paginator = Paginator(properties, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        reviews = Review.objects.filter(property=property, user=request.user)
    else:
        reviews = Review.objects.none() 
    
    state_name = property.location.split(',')[0].strip()
    
    return render(request, 'bdenapp/propertyview.html', {'property':property, 'images':images, 'properties':properties, 'reviews':reviews, 'state_name':state_name, 'page_obj':page_obj})

# Ajax for filtering properties
def ajax_filter_properties(request):
    # Get the price filter from the GET request
    price_filter = request.GET.get('price')
    properties = Property.objects.all()

    # Filter properties based on the selected price range
    if price_filter == 'low':
        properties = properties.filter(price__lt=500000)
    elif price_filter == 'medium':
        properties = properties.filter(price__gte=500000, price__lte=1000000)
    elif price_filter == 'high':
        properties = properties.filter(price__gt=1000000)

    # Serialize filtered properties for JSON response
    property_data = [
        {
            'id': property.id,
            'location': property.location,
            'picture_url': property.picture.url,
            'description': property.description,
            'price': property.price,
        }
        for property in properties
    ]

    return JsonResponse({'properties': property_data})

# properties in a specific city
def properties_by_city(request, city_name):
    filtered_properties = Property.objects.filter(location__icontains=f"{city_name},")
    return render(request, 'bdenapp/city_properties.html', {'city_name':city_name, 'properties':filtered_properties})
# Define a search pattern for the page
def search_results_single(request):
    query = request.GET.get('q')
    if query:
        results = Property.objects.filter(typeChoice__icontains=query)
    else:
        results = Property.objects.none()
    return render(request, 'bdenapp/search_results.html', {'results' : results})

# multiple search patterns
def search_results(request):
    results = PropertyFilter(request.GET, queryset=Property.objects.all())
    # results = None
    return render(request, 'bdenapp/search_results.html', {'results' : results})

# the searched property page
def property_search_result_demo(request):
    results = PropertyFilter(request.GET, queryset=Property.objects.all())
    # results = None
    return render(request, 'bdenapp/property_search_result.html', {'results' : results, 'size' : results.qs.count()})

# Another search pattern to implement
def property_search(request):
    query = request.GET.get('q', '')
    
    results = Property.objects.filter(
        Q(location__icontains=query) | Q(description__icontains=query) | Q(typeChoice__icontains=query)
    )
    
    if results.exists():
        html = ''
        for result in results:
            html += f'<p>{result.location} - {result.typeChoice} - {result.description}</p>'
    else:
        html = '<p>No match found</p>'
    return HttpResponse(html)

    # return render(request, 'bdenapp/property_search_result.html', {'results' : results, 'size' : results.count()})

def property_search_result_backup(request):
    query = request.GET.get('q')
    if query:
        if query != '':
            results = Property.objects.filter(
                Q(location__icontains=query) | Q(description__icontains=query) | Q(typeChoice__icontains=query)
            )
        else:
            results = Property.objects.filter(location__icontains=query)
    
    return render(request, 'bdenapp/property_search_result.html', {'results' : results, 'size' : results.count()})
    
# def the suggestion part of the search query
def search_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        suggestions = Property.objects.filter(
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(typeChoice__icontains=query)
        ).values_list('location', flat=True)[:10]
    else:
        suggestions = []

    return JsonResponse({'suggestions': list(suggestions)})


# Authentication & Authorization 
from payments.models import UserWallet

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        UserWallet.objects.create(user=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'bdenapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home') # Redirect to a home page or dashboard after login
    return render(request, 'bdenapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# is owner users can also list properties
def is_owner_or_superuser(user):
    return user.is_superuser or hasattr(user, 'profile') and user.profile.is_owner


@user_passes_test(is_owner_or_superuser)
def upload_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'bdenapp/upload_property.html', {'form':form})

@user_passes_test(is_owner_or_superuser)
def upload_images(request):
    form = PropertyImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        print(f"Request FILES: {request.FILES}")
        if form.is_valid():
            property_instance = form.cleaned_data.get('property')
            images = request.FILES.getlist('images')

            print(f"Images received: {images}")
            for image in images:
                # image_ins = PropertyImage(images=image)
                # image_ins.save()
                PropertyImage.objects.create(property=property_instance, images=image)
            return redirect('home')
    else:
        form = PropertyImageForm()
    return render(request, 'bdenapp/upload_images.html', {'form': form})


# category view
def category_view(request, category):
    # Filter objects by the first word before the comma in the location field
    filtered_objects = Property.objects.filter(location__startswith=category)
    return render(request, 'bdenApp/category.html', {'objects': filtered_objects})

# handling reviews 

# submiting a reviw
@login_required
def submit_review(request, id):
    property = get_object_or_404(Property, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.property = property
            review.save()
            return redirect('propertyview', id=property.id)
    else:
        form = ReviewForm()
    return render(request, 'bdenapp/submit_review.html', {'form':form, 'property':property})

# user profile creation and things
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

# the user dashboard
@login_required
def user_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    properties = user_profile.user.properties.all
    saved_items = request.user.saveditems_set.all()
    purchases = request.user.purchase_set.all()
    return render(request, 'bdenapp/dashboard.html', {'user_profile':user_profile, 'saved_items':saved_items, 'purchases':purchases, 'properties':properties})

# enabling the owner mode in the dashboard
def is_owner(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    if not userprofile.is_owner:
        userprofile.is_owner = True
        userprofile.save()
    return redirect('dashboard')



# update profile picture
@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm()
    return render(request, 'bdenapp/update_profile_picture.html', {'form':form})

# save an item 
@login_required
def save_for_later(request, id):
    property = get_object_or_404(Property, id=id)
    SavedItems.objects.get_or_create(user=request.user, property=property)
    return redirect('dashboard')

# completing a transaction
@login_required
def complete_purchase(request, id):
    property = get_object_or_404(Property, id=id)
    Purchase.objects.get_or_create(user=request.user, property=property)
    return redirect('dashboard')

# the landing page view
def landing_page(request):
    return render(request, 'bdenapp/landing_page.html', {})

# Deleting a purchase
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_purchase(request, id):
    if request.method == 'POST':
        try:
            purchase = Purchase.objects.get(id=id, user=request.user)
            purchase.delete()
            return JsonResponse({'success': True})
        except Purchase.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Purchase not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# pagenated home view 
from django.core.paginator import Paginator

def home(request):
    properties = Property.objects.all().order_by('location')
    grouped_data = group_and_sort_by_first_word()

    # Convert grouped_data into a list of items for pagination
    grouped_data_items = list(grouped_data.items())

    # Paginate the grouped data (e.g., 10 groups per page)
    paginator = Paginator(grouped_data_items, 12)

    # Get the current page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bdenapp/home.html', {
        'properties': properties,
        'page_obj': page_obj, 
    })

# view for email generation and handling
from django.core.mail import send_mail
from .forms import EmailForm

@login_required
def handle_purchase(request, property_id):
    # Get the property by ID
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Extract owner details from the 'owner' field
    owner_details = property_obj.owner.split(', ')  # Assuming 'name, email, phone' format
    if len(owner_details) == 3:
        owner_name, owner_email, owner_phone = owner_details
    else:
        owner_name, owner_email, owner_phone = "Unknown", "Unknown", "Unknown"

    if request.method == 'POST':
        # Process the submitted form
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            full_message = f"""
            Dear {owner_name},

            {message}

            You can contact me directly via email: {request.user.email} or phone: {request.user.username}.
            """
            
            # Send the email
            send_mail(
                subject,
                full_message,
                request.user.email,  # From the logged-in user's email
                [owner_email],  # To the owner's email
            )

            return render(request, 'bdenapp/success.html', {'property': property_obj})
    else:
        form = EmailForm()

    # Render the form for GET requests
    return render(request, 'bdenapp/purchase_form.html', {
        'form': form,
        'property': property_obj,
        'owner_name': owner_name,
        'owner_phone': owner_phone,
        'owner_email': owner_email,
    })

# Help center page
def help_center(request):
    return render(request, 'bdenapp/features/help_center.html', {})

# live chat view 
def live_chat(request):
    return render(request, 'bdenapp/features/live_chat.html', {})

# report an issue
def report_an_issue(request):
    return render(request, 'bdenapp/features/report_an_issue.html', {})

# the community forum
def community_forum(request):
    return render(request, 'bdenapp/features/community_forum.html', {})

# refunds and cancellation policy
def refunds_and_cancellation(request):
    return render(request, 'bdenapp/features/refunds_and_cancellation.html', {})

# live suggestion view 
def property_autocomplete_backup(request):
    query = request.GET.get('q', '')
    if query:
        suggestions = Property.objects.filter(
            Q(location__icontains=query) | 
            Q(description__icontains=query) |
            Q(typeChoice__icontains=query) 
        ).values_list('typeChoice', flat=True).distinct()
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([], safe=False)

def property_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        suggestions = Property.objects.filter(
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(typeChoice__icontains=query)
        ).values('location', 'typeChoice').distinct()

        # Format the results as "location - typeChoice"
        formatted_suggestions = [
            f"{item['location']} - {item['typeChoice']}"
            for item in suggestions
        ]
        return JsonResponse(formatted_suggestions, safe=False)
    return JsonResponse([], safe=False)

# live search ouput for another search input on the page
def property_autocomplete_view(request):
    query = request.GET.get('q', '')
    if query:
        matches_found = Property.objects.filter(
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(typeChoice__icontains=query)
        ).values('location', 'typeChoice').distinct()

        # Format the results as "location - typeChoice"
        formatted_suggestions = [
            f"{item['location']} - {item['typeChoice']}"
            for item in matches_found
        ]
        return JsonResponse(formatted_suggestions, safe=False)
    return JsonResponse([], safe=False)

# updated property_serach view 

def property_search_result(request):
    query = request.GET.get('q', '')
    price_filter = request.GET.get('price', '')
    results = Property.objects.none()  # Default empty results
    
    if query:
        # Check if query contains the format 'location - typeChoice'
        if ' - ' in query:
            location, type_choice = query.split(' - ', maxsplit=1)
            results = Property.objects.filter(
                Q(location__icontains=location.strip()) & 
                Q(typeChoice__icontains=type_choice.strip())
            )

        else:
            # Search for either location or typeChoice
            results = Property.objects.filter(
                Q(location__icontains=query.strip()) |
                Q(typeChoice__icontains=query.strip()) |
                Q(description__icontains=query.strip())  # Optional fallback
            )
        if price_filter == 'low':
            results = results.filter(price__lt=500000)
        elif price_filter == 'medium':
            results = results.filter(price__gte=500000, price__lte=1000000)
        elif price_filter == 'high':
            results = results.filter(price__gt=1000000)

    return render(request, 'bdenapp/property_search_result.html', {
        'results': results,
        'size': results.count(),
        'query':query,
        'price_filter':price_filter,
    })

# additional filter for price handling
def property_search_result_less(request):
    query = request.GET.get('q', '')
    price_filter = request.GET.get('price', '')  # Capture price filter
    results = Property.objects.none()  # Default to empty results

    if query:
        # Search logic for location, typeChoice, and description
        base_query = Property.objects.filter(
            Q(location__icontains=query.strip()) |
            Q(description__icontains=query.strip()) |
            Q(typeChoice__icontains=query.strip())
        ).distinct()

        # Apply price filter
        if price_filter == 'low':
            results = base_query.filter(price__lt=500000)
        elif price_filter == 'medium':
            results = base_query.filter(price__gte=500000, price__lte=1000000)
        elif price_filter == 'high':
            results = base_query.filter(price__gt=1000000)
        else:
            results = base_query  # No filter applied

    return render(request, 'bdenapp/property_search_result.html', {
        'results': results,
        'size': results.count()
    })

# trending locations view 
def trending_locations(request):
    properties = Property.objects.all()[0:10]
    return render(request, 'bdenapp/features/trending_locations.html', {'properties' : properties})

# new listings 
def new_listings(request):
    return render(request, 'bdenapp/features/new_listings.html', {})

# best deals
def best_deals(request):
    return render(request, 'bdenapp/features/best_deals.html', {})

# user reviews
def user_reviews(request):
    return render(request, 'bdenapp/features/user_reviews.html', {})

# privacy
def privacy(request):
    return render(request, 'bdenapp/features/privacy.html', {})

# terms of service
def terms(request):
    return render(request, 'bdenapp/features/terms.html', {})

# list your property
def list_property(request):
    return render(request, 'bdenapp/features/list_your_property.html', {})

# property management
def property_management(request):
    return render(request, 'bdenapp/features/propertu_management.html', {})

# marketting services
def marketing_services(request):
    return render(request, 'bdenapp/features/mrketing_services.html', {})

# bulk listings
def bulk_listings(request):
    return render(request, 'bdenapp/features/bulk_listings.html', {})

# our mission
def our_mission(request):
    return render(request, 'bdenapp/features/our_mission.html', {})

# the team 
def the_team(request):
    return render(request, 'bdenapp/features/the_team.html', {})

# success_stories
def success_stories(request):
    return render(request, 'bdenapp/features/success_stories.html', {})

# Press and media
def press_and_media(request):
    return render(request, 'bdenapp/features/press_and_media.html', {})



# contact us
def contact_us(request):
    return render(request, 'bdenapp/contact_us.html', {})

# find your dream home
def find_a_property(request):
    return render(request, 'bdenapp/find_a_property.html', {})

# submit your property
def submit_property(request):
    return render(request, 'bdenapp/submit_property.html', {})

# sales form info
def sales_terms(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'bdenapp/sales_terms.html', {'property':property})