from django.urls import path
from . import views

app_name = 'integrations'

urlpatterns = [
    path('',                        views.event_list,  name='events'),
    path('sync/<int:product_id>/',  views.manual_sync, name='manual_sync'),
]