from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('group/', views.group, name='group'),
    path('group/<int:group_id>/', views.group_individual, name='group_individual'),
    path('add_group/', views.add_group, name='add_group'),
    path('delete_group/', views.delete_group_view, name='delete_group_view'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('modify_group_name_view/<int:group_id>/', views.modify_group_name_view, name='modify_group_name_view'),
    path('modify_group_name_submit/<int:group_id>/', views.modify_group_name_submit, name='modify_group_name_submit'),
    path('review_view/<int:group_id>/', views.review_view, name='review_view'),
    path('review_process/<int:review_id>/', views.review_process, name='review_process'),
    path('ajax/review_submit/', views.review_submit, name='review_submit'),
    path('ajax/delete_kanji_from_group/', views.delete_kanji_from_group, name='delete_kanji_from_group'),
    path('review_restart/<int:review_id>/', views.review_restart, name='review_restart'),
    path('review_overview/<int:review_id>/', views.review_overview, name='review_overview'),
]