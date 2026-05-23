from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('',                  views.store_list,   name='list'),
    path('add/',              views.store_add,    name='add'),
    path('<int:pk>/edit/',    views.store_edit,   name='edit'),
    path('<int:pk>/delete/',  views.store_delete, name='delete'),
    path('<int:pk>/logs/',    views.store_logs,   name='logs'),
]