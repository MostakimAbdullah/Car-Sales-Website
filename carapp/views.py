from django.shortcuts import render,redirect
from . import forms
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from carapp.models import CarModel,BrandModel,Comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView,UpdateView
from django.contrib.auth.models import User
from carapp.forms import UserRegisterForm
from django.utils.decorators import method_decorator
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account registration successful')
            return redirect('login')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'type': 'SignUp'})

class SignUpForm(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    def form_valid(self,form):
        messages.success(self.request,'Account registration successfully')
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('home')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'SignUp'
        return context


def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            passwrd = form.cleaned_data['password']
            user = authenticate(username=name, password=passwrd)
            if user is not None:
                login(request,user)
                messages.success(request,'You are now logged in')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form': form, 'type': 'Login'})

class LoginForm(LoginView):
    template_name = 'register.html'
    def form_valid(self,form):
        messages.success(self.request,'Logged in successfully')
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,'Invalid username or password')
        return super().form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('home')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


@login_required
def userlogout(request):
    logout(request)
    messages.success(request,'You are now logged out')
    return redirect('login')



@login_required
def carprofile(request,id):
    data=CarModel.objects.get(pk=id)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = forms.CommentForm()
    carcmt=Comments.objects.all()
    #carcmt=Comments.objects.filter(car=data.name).values()
    return render(request, 'car_details.html', {'data':data,'form': form,'car':carcmt})


cars=[]
@login_required
def buycar(request,id=None):
    data=CarModel.objects.all()
    if id is not None:
        newcar=CarModel.objects.get(pk=id)
        cars.append(newcar)
        if newcar.quantity<0:
            messages.warning(request,f'The car {newcar.name} is out of stock')
            return redirect('home')
        else:
            newcar.quantity-=1
            newcar.save()
            messages.success(request,f'You have successfully bought the car {newcar.name}')
    return render(request, 'profile.html', {'data':cars})
@login_required   
def editprofile(request):
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully')
            return redirect('home')
    else:
        form = forms.EditProfileForm(instance=request.user)
    return render(request, 'register.html', {'form': form, 'type': 'Edit Profile'})

@method_decorator(login_required, name='dispatch')   
class EditProfileView(UpdateView):
    model = User
    form_class = forms.EditProfileForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')
    success_message = "Profile updated successfully"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Edit Profile'
        return context