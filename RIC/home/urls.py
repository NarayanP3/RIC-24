from django.urls import path, reverse_lazy
from . import views


app_name='home'
urlpatterns = [
   path('', views.ProductListView.as_view(),name='home'),
   path('gallery/',views.GalleryView.as_view(),name='gallery'),
   path('event-analytics/', views.event_analytics, name='event_analytics'),
#   path('event-analytics/', views.EventAnalyticsView.as_view(), name='event_analytics'),
   path('all-event-analytics/', views.EventAnalyticsView.as_view(), name='new_event_analytics'),
   path('about', views.AboutList.as_view(),name='about'),
   path('register', views.LoginView.as_view(),name='redirection'),

]