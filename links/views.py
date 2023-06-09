from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Link, Follower, User
from .forms import LinkForm

class HomeView(ListView):
    template_name = 'links/home.html'
    context_object_name = 'links'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            following_users = Follower.objects.filter(user=self.request.user).values_list('followed', flat=True)
            return Link.objects.filter(user__in=following_users).order_by('-shared_at')
        else:
            return Link.objects.none()

class ProfileView(DetailView):
    template_name = 'links/profile.html'
    context_object_name = 'profile_user'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.filter(user=self.object).order_by('-created_at')
        return context

class CustomLoginView(LoginView):
    template_name = 'links/login.html'

def home(request):
    links = Link.objects.all()
    return render(request, 'links/home.html', {'links': links})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('links:home')
    else:
        form = UserCreationForm()
    return render(request, 'links/signup.html', {'form': form})

@login_required
def submit_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('links:home')
    else:
        form = LinkForm()
    return render(request, 'links/submit_link.html', {'form': form})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    links = Link.objects.filter(user=user).order_by('-shared_at')
    return render(request, 'links/profile.html', {'user': user, 'links': links})