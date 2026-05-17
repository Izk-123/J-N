from django.urls import path
from . import views
app_name = 'contacts' 

urlpatterns = [
    path('', views.contact, name='contact'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),   # new
]