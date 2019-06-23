from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('group/', views.group, name='group'),
    path('group/<int:group_id>/', views.group_individual, name='group_individual'),
    path('add_group/', views.add_group, name='add_group'),
]