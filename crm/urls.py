from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='crm-dashboard'),
    path('events/', views.event_list, name='crm-event-list'),
    path('events/edit/<int:event_id>/', views.event_edit, name='crm-event-edit'),
    path('events/add/', views.event_edit, name='crm-event-add'),
    path('events/delete/<int:event_id>/', views.event_delete, name='crm-event-delete'),
    path('login/', views.crm_login, name='crm-login'),
    path('logout/', views.crm_logout, name='crm-logout'),
    path('excursions/', views.excursion_list, name='crm-excursion-list'),
    path('excursions/add/', views.excursion_edit, name='crm-excursion-add'),
    path('excursions/edit/<int:excursion_id>/', views.excursion_edit, name='crm-excursion-edit'),
    path('excursions/delete/<int:excursion_id>/', views.excursion_delete, name='crm-excursion-delete'),
    path('tickets/', views.ticket_list, name='crm-ticket-list'),
    path('tickets/add/', views.ticket_edit, name='crm-ticket-add'),
    path('tickets/edit/<int:ticket_id>/', views.ticket_edit, name='crm-ticket-edit'),
    path('tickets/delete/<int:ticket_id>/', views.ticket_delete, name='crm-ticket-delete'),
    path('users/', views.user_list, name='crm-user-list'),
    path('users/edit/<int:user_id>/', views.user_edit, name='crm-user-edit'),
    path('tickets/export/', views.export_tickets_csv, name='crm-ticket-export'),
    path('users/export/', views.export_users_csv, name='crm-user-export'),
    path('excursions/export/', views.export_excursions_csv, name='crm-excursion-export'),
    path('events/export/', views.export_events_csv, name='crm-event-export'),
    path('excursions/slots/', views.excursion_slot_list, name='crm-excursion-slot-list'),
    path('excursions/slots/add/', views.add_excursion_slot, name='crm-add-slot'),

]
