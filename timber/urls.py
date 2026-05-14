from django.urls import path
from .views import (
    TimberHomeView, TimberAboutView,
    TimberProductsView, TimberProjectsView, TimberContactView
)

app_name = 'timber'

urlpatterns = [
    path('', TimberHomeView.as_view(), name='home'),
    path('about/', TimberAboutView.as_view(), name='about'),
    path('products/', TimberProductsView.as_view(), name='products'),
    path('projects/', TimberProjectsView.as_view(), name='projects'),
    path('contact/', TimberContactView.as_view(), name='contact'),
]
