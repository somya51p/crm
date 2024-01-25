from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('sign-up', views.SignUpAPI.as_view()),
    path('login', views.SignUpAPI.as_view()),
    # path('all-order/', views.UserOrderAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns) + urlpatterns