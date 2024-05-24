from django.shortcuts import render,redirect
from django.views import View
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str as force_text, DjangoUnicodeDecodeError

#from .utils import account_activation_token
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.models import User
from studentPreferences.models import StudentPreferenceModel
from django.contrib.auth.models import Group

@login_required(login_url='login')
def index(request):
    return render(request,'student/index.html')

class Register(View):
    def get(self,request):
        student_form = StudentForm()
        #student_info_form = StudentInfoForm()
        return render(request,'student/register.html',{'student_form':student_form})
    
    def post(self,request):
        student_form = StudentForm(data=request.POST)
        #student_info_form = StudentInfoForm(data=request.POST)
        email = request.POST['email']

        if student_form.is_valid() :
            student = student_form.save()
            student.set_password(student.password)
            #student.is_active = False
            #my_group = Group.objects.get_or_create(name='Student')
            #my_group[0].user_set.add(student)
            student.save()

           
            messages.success(request,"Registered Succesfully. Login")
            
            return redirect('login')
        else:
            print(student_form.errors)
            return render(request,'student/register.html',{'student_form':student_form})
    
class LoginView(View):
	def get(self,request):
		return render(request,'student/login.html')
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']

		if username and password:
			user = auth.authenticate(username=username,password=password)
			if user:
				if user.is_active:
					auth.login(request,user)
					student_pref = StudentPreferenceModel.objects.filter(user = request.user).exists()
					email = User.objects.get(username=username).email

					
					messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")

					return redirect('index')
			
			else:
				user_n = User.objects.filter(username=username).exists()
				if user_n:
					user_v = User.objects.get(username=username)
					if user_v.is_active:
						messages.error(request,'Invalid credentials')	
						return render(request,'student/login.html')
					else:
						messages.error(request,'Account not Activated')
						return render(request,'student/login.html')

		messages.error(request,'Please fill all fields')
		return render(request,'student/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')




	
