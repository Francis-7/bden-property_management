from django.urls import path
from . import views

app_name = 'bdenapp'

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
    path('purchase/<int:property_id>/', views.handle_purchase, name='handle-purchase'),
    path('help',views.help_center, name='help'),
    path('live_chat', views.live_chat, name='live_chat'),
    path('report_your_issue', views.report_an_issue, name='report_issue'),
    path('community_forum', views.community_forum, name='community_forum'),
    path('refunds_and_cancellation_policy', views.refunds_and_cancellation, name='refunds_and_cancellation'),
    path('property_autocomplete', views.property_autocomplete, name='property_autocomplete'),
    path('property_autocomplete_view', views.property_autocomplete_view, name='property_autocomplete_view'),
    path('trending_locations', views.trending_locations, name='trending_locations'),
    path('new_listings', views.new_listings, name='new_listings'),
    path('best_deals', views.best_deals, name='best_deals'),
    path('user_reviews', views.user_reviews, name='user_reviews'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('list_property', views.list_property, name='list_property'),
    path('property_management', views.property_management, name='property_management'),
    path('success_stories', views.success_stories, name='success_stories'),
    path('press_media', views.press_and_media, name='press_media'),
    path('the_team', views.the_team, name='the_team'),
    path('our_mission', views.our_mission, name='our_mission'),
    path('bulk_listings', views.bulk_listings, name='bulk_listings'),
    path('marketting', views.marketing_services, name='marketting'),
    path('properties/<str:city_name>/', views.properties_by_city, name='properties_by_city'),
    path('ajax/filter-properties/', views.ajax_filter_properties, name='ajax_filter_properties'),
    
    
    
    path('is_owner', views.is_owner, name='is_owner'),
    path('contact/us/', views.contact_us, name='contact_us'),
    path('find/your/dream/home/', views.find_a_property, name='find_property'),
    path('submit/property/', views.submit_property, name='submit_property'),
    path('sales/terms/<int:property_id>/', views.sales_terms, name='sales_terms'),
    path('fund/wallet/<int:id>/', views.update_wallet, name='update_wallet'),
]