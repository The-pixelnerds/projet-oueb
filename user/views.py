from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model, login
from django.contrib import messages

def register(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/dashboard')
        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request = request,
        template_name = "user/register.html",
        context={"form":form}
        )


@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html', {'section': 'dashboard'})
