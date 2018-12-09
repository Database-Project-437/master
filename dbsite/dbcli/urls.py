from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('display_q0/', views.handle_0, name='q0'),
	path('display_q1/', views.handle_1, name='q1'),
	path('display_q2/', views.handle_2, name='q2')
]
