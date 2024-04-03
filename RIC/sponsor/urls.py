from django.urls import path, reverse_lazy
from . import views


app_name='sponsor'
urlpatterns = [
    path('', views.SponsorListView.as_view(),name='all'),
    path('register', views.SponsorRegView.as_view(),name='register'),
    path('sponsor_reg_success', views.SponsorRegSuccessView.as_view(),name='sponsor_reg_success'),

]