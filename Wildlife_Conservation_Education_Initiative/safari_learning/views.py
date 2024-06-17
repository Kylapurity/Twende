from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SafariUserCreationForm, SafariUserAuthenticationForm
from django.urls import reverse
from .models import SafariCourse

# Create your views here.

def safari_user_signup(request):
    template_name = "safari_learning/safari_auth.html"
    context_variable = {}
    context_variable["animation"] = "animation"
    if request.method == "POST":
        safari_signup_form = SafariUserCreationForm(data=request.POST)
        if safari_signup_form.is_valid():
            """
            1. Save the form to the model and commit to database,
            2. Then get the cleaned up username, and password, then
            try to get the safari user object, by using the authenticate
            method to see if username exists, and if that password belongs to that username also
            3. Log the safari user in by using the login function i.e putting is_authenticated=True for that safariuser, and assigning the safariuser to the request.user property
            """
            safari_signup_form.save()
            username = safari_signup_form.cleaned_data.get("username")
            password = safari_signup_form.cleaned_data.get("password1")
            safari_user = authenticate(request, username=username, password=password)
            print(safari_user)
            if safari_user:
                login(request, safari_user)
                # TODO redirect user to view name
                print("sending user to homepage")
                return redirect("safari:homepage")

            # if not send user to signup again since authenticate returned none
            context_variable["safari_signup_form"] = SafariUserCreationForm()
            return render(request, template_name, context_variable)
        
        context_variable["safari_signup_form"] = safari_signup_form
        context_variable["safari_form_errors"] = "An error occured when validating this signup form check page for errors made :("
        return render(request, template_name, context_variable)

    # for GET method
    safari_signup_form = SafariUserCreationForm()
    context_variable["safari_signup_form"] = safari_signup_form
    return render(request, template_name, context_variable)

def safari_user_login(request):
    template_name = "safari_learning/safari_auth.html"
    context_variable = {}
    context_variable["animation"] = "animation"
    if request.method == "POST":
        safari_login_form = SafariUserAuthenticationForm(request, data=request.POST)
        if safari_login_form.is_valid():
            # now get the user from the authentication form using .get_user() method
            # then log the user in, then after redirect to home page
            safari_user = safari_login_form.get_user()
            login(request, safari_user)
            # TODO redirect user to home page
            return redirect("safari:homepage")
        
        # if form is not valid give a div hint on the signup or login errors based on the form object
        # sent 
        context_variable["safari_login_form"] = safari_login_form
        context_variable["safari_form_errors"] = "An error occurred when validating this login action username and password are case sensitive"
        return render(request, template_name, context_variable)
    
    # for GET method
    safari_login_form = SafariUserAuthenticationForm(request)
    context_variable["safari_login_form"] = safari_login_form
    return render(request, template_name, context_variable)

def safari_user_homepage(request):
    template_name = "safari_learning/safari_homepage.html"
    context_variable = {}
    if request.user.is_authenticated:
        # TODO show user the homepage
        # TODO also take the necessary data for that page
        # TODO image url, links, based on the profession of the users
        safari_user = request.user
        safari_courses = SafariCourse.objects.filter(
            profession_json__profession__icontains=safari_user.profession,
        ).all()
        print(safari_courses)
        context_variable["safari_user"] = safari_user
        context_variable["safari_courses"] = safari_courses
        return render(request, template_name, context_variable)
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)