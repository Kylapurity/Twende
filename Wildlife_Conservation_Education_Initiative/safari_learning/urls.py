from django.urls import path
from . import views

# Set the app name for namespacing
app_name = 'safari_learning'

# Define the URL patterns for the MonkTraderApp
urlpatterns = [
    # Path for the safari user signup page
    path("safari_user_signup/", views.safari_user_signup, name='signup'),
    # Path for the safari user login page
    path('safari_user_login/', views.safari_user_login, name='login'),
    # Path for homepage
    path("safari_user_homepage/", views.safari_user_homepage, name='homepage'),
]