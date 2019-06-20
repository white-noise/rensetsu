from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:kanji_id>/', views.individual, name='individual'),
    path('<int:kanji_id>/add/', views.add_user, name='add_user')
]