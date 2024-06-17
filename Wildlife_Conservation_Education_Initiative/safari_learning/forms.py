from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import SafariUser
from .models import validate_age

# define the UserCreationForm  for the safari users to register with
class SafariUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SafariUser
        fields = ("first_name", "last_name", "email") + UserCreationForm.Meta.fields + ("age", "profession")


"""
Define the Authentication Form for the safari users

This form authenticates with the backends provided by django settings
but it uses the user model set to the settings.AUTH_USER_MODEL
to do some validations which are;
The AuthenticationForm performs several internal validations:

1. Username Existence: It checks whether the provided username exists in the database.
2. Password Matching: It verifies if the provided password matches the stored hashed password for the given username. This is done using Django's authenticate function.

The AuthenticationForm provides two fields:

1. username
2. password
"""
class SafariUserAuthenticationForm(AuthenticationForm):
    pass