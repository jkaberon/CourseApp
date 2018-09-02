from django.urls import path
from . import views

urlpatterns = [path('out',views.index,name='index'),
				path('in',views.input,name='input')]

