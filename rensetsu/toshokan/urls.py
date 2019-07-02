from django.urls import path

from . import views

app_name = 'toshokan'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:kanji_id>/', views.individual, name='individual'),
    path('<int:kanji_id>/interesting/', views.toggle_interesting, name='toggle_interesting'),
    path('<int:kanji_id>/difficult/', views.toggle_difficult, name='toggle_difficult'),
    path('<int:kanji_id>/known/', views.toggle_known, name='toggle_known'),
    path('<int:kanji_id>/comment/', views.comment, name='comment'),
    path('<int:kanji_id>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:kanji_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('<int:kanji_id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('<int:kanji_id>/modify_comment/<int:comment_id>/', views.modify_comment, name='modify_comment'),
    path('<int:kanji_id>/groups/', views.kanji_group_view, name='kanji_group_view'),
    path('<int:kanji_id>/delete_from_group/', views.kanji_delete_group_view, name='kanji_delete_group_view'),
    path('<int:kanji_id>/groups/<int:group_id>/', views.add_kanji_to_group, name='add_kanji_to_group'),
    path('<int:kanji_id>/remove_group/<int:group_id>/', views.remove_kanji_from_group, name='remove_kanji_from_group'),
]