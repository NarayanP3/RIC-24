from django.urls import path
from .views import ViewAllRICEventsView, ChangeStatusView, ViewRICEventSubmissionView

app_name = 'editor'

urlpatterns = [
    path('', ViewAllRICEventsView.as_view(), name='view_all_ricevents'),
    path('change_status/<int:event_id>/', ChangeStatusView.as_view(), name='change_status'),
    path('view/<int:event_id>/', ViewRICEventSubmissionView.as_view(), name='view_submission'),
]
