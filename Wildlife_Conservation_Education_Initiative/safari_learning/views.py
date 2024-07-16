from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SafariUserCreationForm, SafariUserAuthenticationForm, SafariForm, EventForm
from django.urls import reverse
from .models import SafariCourse, Interest, SafariUser, Event, BookedEvent
from django.http import JsonResponse
import json

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
                return redirect("safari:landing_page")

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
            return redirect("safari:landing_page")
        
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
        print(safari_user.profession)
        safari_courses = SafariCourse.objects.filter(
            profession_json__profession__icontains=safari_user.profession,
        ).all()
        print(safari_courses)
        context_variable["safari_user"] = safari_user
        context_variable["safari_courses"] = safari_courses
        return render(request, template_name, context_variable)
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)

def safari_user_interests(request, user_id):
    template_name_1 = "safari_learning/interests.html"
    template_name_2 = "safari_learning/interesterror.html"
    context_variable = {}

    if request.user.is_authenticated:
        if request.method == "GET":
            if request.user.id != user_id:
                return render(request, template_name_2)
            # get the actual user interest and also get all interest
            user_interests = request.user.interests
            if user_interests:
                user_interests = user_interests.get("interests", [])
            else:
                user_interests = []
            all_interests = Interest.objects.all()
            all_courses = SafariCourse.objects.all()
            print(all_courses) 
            recommended_courses = [recommended_course for recommended_course in all_courses if set(user_interests).intersection(recommended_course.course_tags.get("course_tags"))]
            context_variable["recommended_courses"] = recommended_courses
            context_variable["user_interests"] = user_interests
            context_variable["all_interests"] = all_interests
            context_variable["logged_in_user"] = request.user
            return render(request, template_name_1, context_variable)
        
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)

def safari_user_clicked_interest(request, user_id):
    template_name = "safari_learning/interests.html"
    context_variable = {}

    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.id != int(user_id):
                return JsonResponse({'status': 'error', 'message': reverse("safari_learning:error_view")}, status=403)
            # get the actual user interest and also get all interest
            try:
                # Read and parse the JSON data from the request body
                data = json.loads(request.body.decode('utf-8'))
                get_interest = data.get('interest').strip()
                """
                before you return the response save this interest to
                the user authenticated interest json
                """
                get_user = SafariUser.objects.filter(
                    id=user_id
                ).first()

                if not get_user.interests:
                    interest_list = []
                    interest_list.append(get_interest)
                    interest_dict = {"interests": interest_list}
                    request.user.interests = interest_dict
                    request.user.save()
                else:
                    interest_dict = request.user.interests
                    print(interest_dict)
                    interest_dict.get("interests").append(get_interest)
                    print(interest_dict)
                    request.user.interests = interest_dict
                    request.user.save()
                
                response_data = {
                    "status": "OK",
                    "code": 200,
                    "data": get_interest,
                    "statusText": "success",
                }
                return JsonResponse(response_data)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
        if request.method == "GET":
            # get the actual user interest and also get all interest
            user_interests = request.user.interests
            if user_interests:
                user_interests = user_interests.get("interests", [])
            
            all_interests = Interest.objects.all()
            all_courses = SafariCourse.objects.all()
            recommended_courses = [recommended_course for recommended_course in all_courses if set(user_interests).intersection(recommended_course.course_tags.get("course_tags"))]
            context_variable["recommended_courses"] = recommended_courses
            context_variable["user_interests"] = user_interests
            context_variable["all_interests"] = all_interests
            context_variable["logged_in_user"] = request.user
            return render(request, template_name, context_variable)

        
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)

def safari_user_delete_interest(request, user_id):
    template_name = "safari_learning/interests.html"
    context_variable = {}

    if request.user.is_authenticated:
        if request.method == "DELETE":
            if request.user.id != int(user_id):
                return JsonResponse({'status': 'error', 'message': reverse("safari_learning:error_view")}, status=403)
            # get the actual user interest and also get all interest
            try:
                # Read and parse the JSON data from the request body
                data = json.loads(request.body.decode('utf-8'))
                get_interest = data.get('interest').strip()
                """
                before you return the response save this interest to
                the user authenticated interest json
                """
                get_user = SafariUser.objects.filter(
                    id=user_id
                ).first()

                if not get_user.interests:
                    pass
                else:
                    interest_dict = request.user.interests
                    interest_dict.get("interests").remove(get_interest)
                    request.user.interests = interest_dict
                    request.user.save()
                
                response_data = {
                    "status": "OK",
                    "code": 200,
                    "data": get_interest,
                    "statusText": "success",
                }
                return JsonResponse(response_data)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
        if request.method == "GET":
            # get the actual user interest and also get all interest
            user_interests = request.user.interests
            if user_interests:
                user_interests = user_interests.get("interests", [])
            
            all_interests = Interest.objects.all()
            all_courses = SafariCourse.objects.all()
            recommended_courses = [recommended_course for recommended_course in all_courses if set(user_interests).intersection(recommended_course.course_tags.get("course_tags"))]
            context_variable["recommended_courses"] = recommended_courses
            context_variable["user_interests"] = user_interests
            context_variable["all_interests"] = all_interests
            context_variable["logged_in_user"] = request.user
            return render(request, template_name, context_variable)  

        
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)

def safari_error_view(request):
    template_name = "safari_learning/interesterror.html"
    return render(request, template_name)


def BookEventView(request):
    template_name = "safari_learning/event_book.html"
    context_variable = {}
    if request.user.is_authenticated:
        if request.method == "GET":
            safari_form = SafariForm({
                "username": request.user.username,
                "email": request.user.email,
            })
            event_form = EventForm()
            context_variable["safari_form"] = safari_form
            context_variable["event_form"] = event_form
            if request.session.get("success_msg", None):
                context_variable["success_msg"] = request.session["success_msg"]
                del request.session["success_msg"]
            return render(request, template_name, context_variable)
        
        if request.method == "POST":
            get_username = request.POST.get("username")
            get_email = request.POST.get("email")
            get_event = request.POST.get("event_name")

            if request.user.username != get_username or request.user.email != get_email:
                safari_form = SafariForm({
                    "username": request.user.username,
                    "email": request.user.email,
                })
                event_form = EventForm()
                context_variable["safari_form"] = safari_form
                context_variable["event_form"] = event_form
                context_variable["error_msg"] = "The username and email should be of the user logged in !!!"      
                return render(request, template_name, context_variable)
            # check if the request.user has already exists by using the 
            # event_name and the request.user
            event_object = Event.objects.filter(
                event_name=get_event.strip(),
            )
            book_event_object = BookedEvent.objects.filter(
                user=request.user,
                events=event_object.first(),
            )

            if book_event_object.exists():
                safari_form = SafariForm({
                    "username": request.user.username,
                    "email": request.user.email,
                })
                event_form = EventForm()
                context_variable["safari_form"] = safari_form
                context_variable["event_form"] = event_form
                context_variable["error_msg"] = "You have already booked for this event!!!"      
                return render(request, template_name, context_variable)              
            # if all is save that booked event for  user
            BookedEvent.objects.create(
                user=request.user,
                events=event_object.first(),
            )
            request.session["success_msg"] = "Event has been booked :)"
            return redirect(request.path)
        
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)


def LandingView(request):
    template_name = "safari_learning/safari_landingpage.html"
    context_variable = {}
    if request.user.is_authenticated:
        context_variable["logged_in_user"] = request.user
        return render(request, template_name, context_variable)
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)

def FAQView(request):
    template_name = "safari_learning/faq_page.html"
    context_variable = {}
    if request.user.is_authenticated:
        context_variable["logged_in_user"] = request.user
        return render(request, template_name, context_variable)
    redirectback_here_link = reverse("safari:login")
    return redirect(redirectback_here_link)
