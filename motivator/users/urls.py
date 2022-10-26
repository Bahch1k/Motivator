
from django.urls import include, path
from .views import Register, get_motivations, get_form_data, DetailMotivationList

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('motivations/', get_motivations, name='main'),
    path('motivations/new', get_form_data, name='motivations'),
    path('motivations/<int:id>', DetailMotivationList.as_view())
]
