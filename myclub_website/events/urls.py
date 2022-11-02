from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events/', views.list_events, name='list_events'),
    path('add_venue/', views.add_venue, name='add_venue'),
    path('list_venues/', views.list_venues, name='list_venues'),
    path('show_venue/<venue_id>/', views.show_venue, name='show_venue'),
    path('search_venues', views.search_venues, name='search_venues'),
    path('update_venue/<venue_id>/', views.update_venue, name='update_venue'),
    path('add_event/', views.add_event, name='add_event'),
    path('update_event/<event_id>/', views.update_event, name='update_event'),
    path('delete_event/<event_id>/', views.delete_event, name='delete_event'),
    path('delete_venue/<venue_id>/', views.delete_venue, name='delete_venue'),
    path('venue_text', views.venue_text, name='venue_text'),
    path('venue_csv', views.venue_csv, name='venue_csv'),
    path('venue_pdf', views.venue_pdf, name='venue_pdf'),
]