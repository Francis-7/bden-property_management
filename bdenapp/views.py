from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, PropertyImage
from .filters import PropertyFilter
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, PropertyForm, PropertyImageForm


def home(request):
    properties = Property.objects.all().order_by('location')
    return render(request, 'bdenapp/home.html', {'properties': properties})

def propertyView(request, id):
    property = get_object_or_404(Property, id=id)
    images = property.propertyimage_set.all()
    return render(request, 'bdenapp/propertyview.html', {'property':property, 'images':images})

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

def property_search_result(request):
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

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
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


@user_passes_test(lambda u: u.is_superuser)
def upload_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.save()
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'bdenapp/upload_property.html', {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def upload_images(request):
    if request.method == 'POST':
        form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.cleaned_data.get('property')  # Get the property instance
            images = request.FILES.getlist('images')  # Get all uploaded images

            for img in images:
                PropertyImage.objects.create(property=property_instance, images=img)
            return redirect('home')  # Ensure the home URL is defined in urls.py
        else:
            print("Form errors:", form.errors)  # Debug form errors
    else:
        form = PropertyImageForm()

    return render(request, 'bdenapp/upload_images.html', {'form': form})