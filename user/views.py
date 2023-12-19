from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib import messages
from .models import UserPermission

def register(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            #on creer le userPermission en meme temps
            userPermission = UserPermission(user=user, permissionInteger=0)
            userPermission.save()

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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/password_change_form.html', {
        'form': form
    })