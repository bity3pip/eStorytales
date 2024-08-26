from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from accounts.forms import CustomLoginForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('books-list')

    form = CustomLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                remember = form.cleaned_data.get('remember')
                if remember:
                    request.session.set_expiry(604800)
                else:
                    request.session.set_expiry(0)

                return redirect('books-list')

            else:
                form.add_error(None, 'Invalid username or password.')

        else:
            messages.error(request, 'Please correct the error below.')

    return render(request, 'registration/login.html', {'form': form})
