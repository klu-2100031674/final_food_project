from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
#to activate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from .utils import TokenGenerator,generate_token
#emails
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.core.mail.message import EmailMessage
from math import ceil
import json
from django.views.decorators.csrf import  csrf_exempt
#reset password generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
MERCHANT_KEY = 'addyour key'
import threading
class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()
def signupforadmin(request):
    if request.method == 'POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 != password2:
            messages.error(request,"Password do not Match,Please Try Again!")
            return redirect('/foodauth/signup')
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/foodauth/signupforadmin')
        except Exception as identifier:            
            pass 
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/foodauth/signup')
        except Exception as identifier:
            pass        
        user = User.objects.create_user(email,email,password1)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active=False
        user.is_staff=True
        user.save()
        cuurrent_site=get_current_site(request)
        email_subject="Activate your account"
        message=render_to_string('auth/activate.html',{  
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request," Activate your account in mail bor(check spam)")
        return redirect('/foodauth/loginforadmin')
    return render(request,'auth/signupforadmin.html')

def signup(request):
     if request.method == 'POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 != password2:
            messages.error(request,"Password do not Match,Please Try Again!")
            return redirect('/foodauth/signup')
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/foodauth/signup')
        except Exception as identifier:            
            pass 
        try:
            if User.objects.get(mobile_number=mobile_number):
                messages.warning(request,"Mobile number is Already Exists")
                return redirect('/foodauth/signup')
        except Exception as identifier:
            pass   
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/foodauth/signup')
        except Exception as identifier:
            pass        
        # checks for error inputs
        user = User.objects.create_user(email,email,password1)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active=False
        user.save()
        cuurrent_site=get_current_site(request)
        email_subject="Activate your account"
        message=render_to_string('auth/activate.html',{  
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request," Activate your account in mail bor(check spam)")
        return redirect('/foodauth/login')
     return render(request,'auth/register.html')
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated successfully")
            return redirect('/foodauth/login')
        return render(request,'auth/activatefail.html') 
def Handlelogin(request):
    if request.method == 'POST':
        loginusername=request.POST['email']
        loginpassword=request.POST['password']
        user=authenticate(username=loginusername,password=loginpassword)
       
        if user is not None and user.is_staff == True:
            login(request,user)
            return redirect('/admin')
        elif user is not None and user.is_staff == False:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/foodauth/login')    
    return render(request,'auth/login.html')
def Handlelogouts(request):
    logout(request)
    messages.warning(request,"Logout Success")
    return render(request,'auth/login.html')
class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'auth/request-reset-email.html')
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            current_site=get_current_site(request)
            email_subject=['Reset your password']
            message=render_to_string('auth/reset-user-password.html',
            {
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])

            })
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            EmailThread(email_message).start()
            messages.info(request,"we sent a email to reset the password")
            return render(request,'auth/request-reset-email.html')
class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"password reset link is invalid")
                return render(request,'auth/request-reset-email.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        return render(request,'auth/set-new-password.html',context)
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token,
        }

        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 != password2:
            messages.error(request,"Password do not Match,Please Try Again!")
            return render(request,'auth/set-new-password.html',context)
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request,"password successfully change login into your account ")
            return redirect('/foodauth/login/')
        except DjangoUnicodeDecodeError as idetifier:
            messages.error(request,"some thing went wrong")
            return render(request,'auth/set-new-password.html',context)

        return render(request,'auth/set-new-password.html',context)
