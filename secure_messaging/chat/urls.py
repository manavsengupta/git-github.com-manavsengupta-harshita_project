from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),               # The new landing page
    path('inbox/', views.inbox, name='inbox'),         # Moved inbox to /inbox/
    path('send/', views.send_message, name='send_message'),
]