from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('webhook', views.webhook, name='webhook'),
    path('web', views.web, name='web')
]