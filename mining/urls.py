from django.urls import path
from .views import (
    MiningHomeView, MiningAboutView,
    MiningMineralsView, MiningOperationsView, MiningContactView
)

app_name = 'mining'

urlpatterns = [
    path('', MiningHomeView.as_view(), name='home'),
    path('about/', MiningAboutView.as_view(), name='about'),
    path('minerals/', MiningMineralsView.as_view(), name='minerals'),
    path('operations/', MiningOperationsView.as_view(), name='operations'),
    path('contact/', MiningContactView.as_view(), name='contact'),
]
