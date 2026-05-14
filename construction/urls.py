from django.urls import path
from .views import (
    ConstructionHomeView, ConstructionAboutView,
    ConstructionServicesView, ConstructionProjectsView,
    ConstructionProjectDetailView, ConstructionContactView
)

app_name = 'construction'

urlpatterns = [
    path('', ConstructionHomeView.as_view(), name='home'),
    path('about/', ConstructionAboutView.as_view(), name='about'),
    path('services/', ConstructionServicesView.as_view(), name='services'),
    path('projects/', ConstructionProjectsView.as_view(), name='projects'),
    path('projects/<slug:slug>/', ConstructionProjectDetailView.as_view(), name='project_detail'),
    path('contact/', ConstructionContactView.as_view(), name='contact'),
]
