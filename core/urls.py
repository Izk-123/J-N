from django.urls import path
from .views import HomeView, AboutView
from .dashboard import AdminDashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]