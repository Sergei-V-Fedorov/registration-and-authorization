from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm, ProfileForm
from .models import Profile
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class LoginFormView(LoginView):
    template_name = 'users/login.html'


class LogoutFormView(LogoutView):
    next_page = reverse_lazy('news')


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        profile = Profile.objects.get(user_id=user_id)
        context['news_published'] = profile.news_published
        return context


class ProfileFormEdit(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    fields = ['birthdate', 'city', 'telephone']
    template_name_suffix = '_edit_form'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.object.user_id)
        profile = Profile.objects.get(pk=self.object.pk)
        first_name = user.first_name
        last_name = user.last_name
        form = ProfileForm(instance=profile, initial={'first_name': first_name, 'last_name': last_name})
        context['form'] = form
        return context

    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(id=pk)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.get(profile=pk)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            form.save()
            return redirect(reverse('profile-edit', args=[pk]))
        return render(request, reverse('profile-edit', args=[pk]),
                      {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            birthdate = form.cleaned_data.get('birthdate')
            city = form.cleaned_data.get('city')
            telephone = form.cleaned_data.get('telephone')
            Profile.objects.create(user=user, birthdate=birthdate,
                                   city=city, telephone=telephone)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('news'))
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
