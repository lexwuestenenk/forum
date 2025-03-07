from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from django.views import View

# Create your views here.
class SignupView(View):
    template_name = 'accounts/signup.html'
    
    def get(self, request):
        user_creation_form = UserCreationForm
        return render(
            request,
            self.template_name,
            {
                'user_creation_form': user_creation_form
            }
        )
        
    def post(self, request):
        user_creation_form = UserCreationForm(request.POST)
        
        if user_creation_form.is_valid():
            user_creation_form.save()
        
        return redirect(reverse('login'))
        
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = '/'
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('question-list'))