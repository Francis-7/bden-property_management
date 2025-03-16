from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('propertyview/<int:id>/', views.propertyView, name='propertyview'),
    path('search/', views.search_results, name='search_results'),
    path('property_search_result', views.property_search_result, name='property_search_result'),
    path('search_suggestions', views.search_suggestions, name='search_suggestions'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('upload_property', views.upload_property, name='upload_property'),
    path('upload_images', views.upload_images, name='upload_images'),
    path('property_search/', views.property_search, name='property_search'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('submit_review/<int:id>/', views.submit_review, name='submit_review'),
    path('update_profile_picture', views.update_profile_picture, name='update_profile_picture'),
    path('dashboard', views.user_dashboard, name='dashboard'),
    path('save_for_later/<int:id>', views.save_for_later, name='save_for_later'),
    path('landing_page', views.landing_page, name='landing_page'),
    path('purchase/<int:id>', views.complete_purchase, name='purchase'),
    path('delete-purchase/<int:id>/', views.delete_purchase, name='delete-purchase'),
]