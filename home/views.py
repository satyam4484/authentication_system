from django import http
from django.contrib.auth import authenticate, update_session_auth_hash
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib import messages
from django.utils import html
from .forms import loginform,signupform,resetform,passwordchange,newpasswordform
from django.contrib.auth.models import User
from .models import userprofile
import uuid
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
def home(request):
    # messages.success(request,'welcome to authentication system testing')
    return render(request,'home.html')

# ************************ Login user *****************************************************

def sendmail_to_user(email,subject,message):
    emailfrom = settings.EMAIL_HOST_USER
    send_mail(subject,message,emailfrom,[email,])



def loginUser(request):
    ''' These is the function for login user '''
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginform(request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                userobj = User.objects.filter(username=username).first()
                profileobj = userprofile.objects.filter(user = userobj).first()
                if profileobj.is_verified:
                    user = authenticate(username=username,password=password)
                    if user :
                        login(request,user)
                        messages.success(request,'You are successfully logined')
                        return HttpResponseRedirect('/')
                else :
                    messages.error(request,'Please verify your email')
                    return HttpResponseRedirect('/login')
            else:
                messages.error(request,'Enter valid details')
        else :
            form = loginform()
    
        context = {
            'form':form,
            'name':'Login Form',
            'value':"Don't have an account ? create here",
            'pss':1,

        }
        return render(request,'login.html',context)
    else :
        messages.warning(request,'you are already logged in')
        return HttpResponseRedirect('/')
    
# ******************************************************************************************************





# ***************************** Sign up user ************************************************************

def verifyuser(request,token):
    try :
        profile = userprofile.objects.filter(email_verify=token).first()
        if profile:
            profile.is_verified = True
            profile.save()
            messages.success(request,'you may now login')
            return HttpResponseRedirect('/login')
        else :
            messages.error(request,'please create an account!')
            return HttpResponseRedirect('/signup')
    except Exception as e:
        print(e)
    return HttpResponseRedirect('/signup')


def SignupUser(request):
    ''' This is for user sign up '''
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = signupform(request.POST)            
            if form.is_valid():
                email = form.cleaned_data['email']
                form.save() 
                userobj = User.objects.filter(email = email).first()
                token = str(uuid.uuid4())
                profile = userprofile.objects.create(user = userobj,email_verify=token)
                profile.save()
                subject = f"Hi {userobj.username} , You need to verify your email before login ."
                message = f"Please click the link to verify it http://127.0.0.1:8000/verify/{token}"
                sendmail_to_user(email,subject,message)
                messages.info(request,'Check your mail verify your account ')
                return HttpResponseRedirect('/signup')
        else :
            form = signupform()
        context = {
            'form':form,
            'name':'Signup Form',
            # 'value':"Already have an account?  login here",
            'pss':0,

        }
        return render(request,'login.html',context)
    else :
        messages.info(request,'You are already logged in')
        return HttpResponseRedirect('/')

# *****************************************************************************************



# ****************** Logout user ***************************************

def logoutUser(request):
    logout(request)
    messages.warning(request,'Logged out successfully')
    return HttpResponseRedirect('/')

# ***************************************************************************



# ************************** Reset password  *****************************************************
def resetpass(request):
    if request.method == 'POST':
        form = newpasswordform(request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.cleaned_data['username'])
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successfully! you may login now')
            return HttpResponseRedirect('/login')
    else :
        form = newpasswordform()
    
    context = {
            'form':form,
            'name':'Update Password form',
            'pss':0,

        }
    return render(request,'login.html',context)


def verifyr(request,token):
    try :
        profile = userprofile.objects.filter(reset_pass_token=token).first()
        if profile:
            profile.is_verified = True
            profile.save()
            messages.info(request,'Enter details')
            return HttpResponseRedirect('/reset')
        else :
            messages.error(request,'Username does  not exist')
            return HttpResponseRedirect('/signup')
    except Exception as e:
        print(e)
    return HttpResponseRedirect('/signup')


def resetPasswordUser(request):
    if request.method == 'POST':
        form = resetform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = User.objects.filter(username=username).first()
            if user:
                profile = userprofile.objects.filter(user = user).first()
                token = str(uuid.uuid4())
                profile.reset_pass_token = token
                profile.save()
                subject = f"Hi {user.username} , You need to verify your email to change password ."
                message = f"Please click the link to verify it http://127.0.0.1:8000/verifyr/{token}"
                sendmail_to_user(email,subject,message)
                messages.info(request,'Check your mail verify your account ')
                return HttpResponseRedirect('/login')
            else :
                messages.error(request,'user does not exist')
                return HttpResponseRedirect('/signup')
    else :
        form =resetform()
    
    context = {
            'form':form,
            'name':'Reset password form',
            'pss':0,
    }

    return render(request,'login.html',context)

# *******************************************************************************************************



#******************************   change password  ********************************************************
def ChangePasswordUser(request):
    if request.method == 'POST':
        form = passwordchange(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'password changed successfully')
            return HttpResponseRedirect('/')
    else :
        form = passwordchange(request.user)
    
    context = {
        'form':form,
        'name':'Change password form',
        'pss':0,
    }
    return render(request,'login.html',context)

# **************************************************************************************************************