from django.urls import path
from .views import HomeView, AboutView, log_whatsapp_click
from .dashboard import dashboard_messages_api, dashboard_stats_api, dashboard_visitors_api, htmx_mark_message_read, htmx_mark_message_replied, htmx_toggle_featured

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    
    # HTMX endpoints
    path('htmx/message/<int:pk>/read/',    htmx_mark_message_read,    name='htmx_message_read'),
    path('htmx/message/<int:pk>/replied/', htmx_mark_message_replied,  name='htmx_message_replied'),
    path('htmx/toggle/<str:model>/<int:pk>/featured/', htmx_toggle_featured, name='htmx_toggle_featured'),
    
    # Dashboard live data endpoints
    path('admin/dashboard/stats/',    dashboard_stats_api,    name='dashboard_stats_api'),
    path('admin/dashboard/messages/', dashboard_messages_api, name='dashboard_messages_api'),
    path('admin/dashboard/visitors/', dashboard_visitors_api, name='dashboard_visitors_api'),
    
    path('log-whatsapp-click/', log_whatsapp_click, name='log_whatsapp_click'),
]