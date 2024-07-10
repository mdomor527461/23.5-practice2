from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import forms
from django.views.generic import FormView,UpdateView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = forms.UserRegistrationForm
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:  
#             logout(self.request)
#         return reverse_lazy('home')

def user_logout(request):
    logout(request)
    return redirect('home')

class UserUpdateView(UpdateView):
    template_name = 'accounts/profile.html'
    
    def get(self,request):
        form = forms.UserUpdateForm(instance = request.user)
        return render(request,self.template_name,{'form' : form})
    
    def post(self,request):
        form = forms.UserUpdateForm(request.POST,instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request,self.template_name,{'form' : form})
        
        
        
