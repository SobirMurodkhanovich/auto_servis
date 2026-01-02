from django.urls import path
from .views import (
    index_page, employee_view, login_view,
    auto_add_view, auto_list_view, auto_edit_view, auto_delete_view,
    services_view, services_add_view, services_edit, services_delete,
    auto_service_page, history_view, history_detail_view
)

urlpatterns = [
    path('', index_page, name='index-page'),
    path('login-page/', login_view, name='login-page'),
    path('employee-page/', employee_view, name='employee-page'),
    path('auto-list/', auto_list_view, name='auto-list'),
    path('auto-add/', auto_add_view, name='auto-add'),
    path('avto-edit/<int:pk>/', auto_edit_view, name='avto-edit'),
    path('auto-delete/<int:pk>/', auto_delete_view, name='auto-delete'),

    path('services/', services_view, name='services-page'),
    path('services-add/', services_add_view, name='services-add'),
    path('services-edit/<int:pk>/', services_edit, name='services-edit'),
    path('services-delete/<int:pk>/', services_delete, name='services-delete'),

    path('car-services/', auto_service_page, name='car-services-page'),

    path('history/', history_view, name='history-page'),
    path('history-detail/<int:pk>/', history_detail_view, name='history-detail'),
]
