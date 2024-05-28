from django.shortcuts import render,redirect
from django.views import View
from .forms import FacultyForm
from .models import FacultyInfo
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import threading
from django.contrib.sites.shortcuts import get_current_site
#from student.views import EmailThread
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from questions.views import has_group
from django.http import HttpResponseRedirect
from django.urls import reverse
from student.models import StuResults_DB
from django.http import HttpResponse



@login_required(login_url='faculty-login')
def index(request):
    return render(request,'faculty/index.html')

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib import messages


def view_student_results(request):
    try:
        # Fetch all student results with related student and exams data
        results = StuResults_DB.objects.all().select_related('student').prefetch_related('exams')

        # Check if there are any results
        if not results.exists():
            return HttpResponse("No results found", status=404)
        
        # Prepare the context dictionary
        context = {
            'results': results
        }

        # Render the template with the context data
        return render(request, 'faculty/view_results.html', context)
    
    except StuResults_DB.DoesNotExist:
        # Handle the case where the StuResults_DB model does not exist
        return HttpResponse("Error: Student results not found", status=500)
    
    except Exception as e:
        # Handle any other exceptions
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


class Register(View):
    def get(self, request):
        faculty_form = FacultyForm()
        return render(request, 'faculty/register.html', {'faculty_form': faculty_form})
    
    def post(self, request):
        faculty_form = FacultyForm(data=request.POST)
        if faculty_form.is_valid():
            faculty = faculty_form.save(commit=False)
            faculty.set_password(request.POST['password'])  # Manually set password
            faculty.is_active = True
            faculty.is_staff = True
            faculty.save()
            messages.success(request, "Registered successfully. Login now.")
            return redirect('faculty-login')
        else:
            # Display specific error messages for each field
            errors = faculty_form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect('faculty-register')  # Redirect back to registration page with error messages


    
class LoginView(View):
    def get(self, request):
        return render(request, 'faculty/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None :
                auth.login(request, user)
                messages.success(request, "Welcome, " + user.username + ". You are now logged in.")
                return redirect('faculty-index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please fill all fields')

        return render(request, 'faculty/login.html')


            

		

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('homepage')