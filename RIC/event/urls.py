from django.urls import path, reverse_lazy
from . import views
from .views import merchandise_view


app_name='event'
urlpatterns = [
    # path('<int:pk>', views.ProductDetail.as_view(),name='detail'),
    
    # path('workshopspeaker/<int:pk>', views.SpeakerDetail.as_view(),name='workshopspeakerspeaker'),
    path('speaker/', views.DeptSpeakerListView.as_view(),name='speakerlist'),
    path('merch/', merchandise_view,name='merch'),
    path('speaker/<int:pk>', views.SpeakerDetailView.as_view(),name='speakerdetail'),
    path('deptspeaker/<int:pk>', views.DeptSpeakerDetailView.as_view(),name='deptspeakerdetail'),
    path('<slug:name>/', views.ProductDetail.as_view(),name='detail'),
]