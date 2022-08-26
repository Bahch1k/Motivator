
from django.urls import include, path
from .views import Register, MotivationList, add_motivation, DetailMotivationList

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('motivations/', MotivationList.as_view(), name='main'),
    path('motivations/new', add_motivation, name='motivations'),
    path('motivations/<int:id>', DetailMotivationList.as_view())
]
