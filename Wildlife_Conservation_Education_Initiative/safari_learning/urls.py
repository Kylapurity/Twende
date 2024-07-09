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
    path("interests/<int:user_id>/", views.safari_user_interests, name='interests'),
    path("clickedinterest/<int:user_id>/", views.safari_user_clicked_interest, name='clickedinterest'),
    path("deleteinterest/<int:user_id>/", views.safari_user_delete_interest, name='deleteinterest'),
    path("error_view/", views.safari_error_view, name='error_view'),
    path("book_event/", views.BookEventView, name='book_event'),
    path("landing_page/", views.LandingView, name='landing_page'),
    path("faq_page/", views.FAQView, name='faq_page'),
]