from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:kanji_id>/', views.individual, name='individual'),
    path('<int:kanji_id>/interesting/', views.toggle_interesting, name='toggle_interesting'),
    path('<int:kanji_id>/difficult/', views.toggle_difficult, name='toggle_difficult'),
    path('<int:kanji_id>/known/', views.toggle_known, name='toggle_known'),
]