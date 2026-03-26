from django.urls import path
from app import views

urlpatterns = [
    path('', views.route_list, name='route_list'),
    path('add-airport/', views.add_airport, name='add_airport'),
    path('add/', views.add_route, name='add_route'),
    path('longest/', views.longest_route, name='longest_route'),
    path('shortest/', views.shortest_route, name='shortest_route'),
    path('nth/', views.nth_route, name='nth_route'),
    path('tree/', views.route_tree, name='route_tree'),
]