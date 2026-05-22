from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm
from django.contrib.auth.views import PasswordChangeView
from .forms import UserPasswordChangeForm
from django.conf import settings

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Change Password'}

# Login view (class-based)
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization'}

    def get_success_url(self):
        return reverse_lazy('home')

# Registration view using CreateView and UserCreationForm
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('users:login')

# Profile view (edit user's own profile)
class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'User Profile', 'default_image': settings.MEDIA_URL + 'users/default.png'}

    def get_object(self, queryset=None):
        # Return the currently logged‑in user
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')