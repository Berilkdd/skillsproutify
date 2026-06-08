from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from learning.models import JobRole


def home(request):
    """
    Renders the public home page for the users.
    """
    return render(request, 'home.html')


@login_required
def login_redirect(request):
    """
    Redirects the user to dashboard or welcome page after login based on roles.
    """
    if request.user.jobrole_set.exists():
        # If they already have some roles selected
        return redirect('selected_roles')
    # If they haven't got any role yet
    return redirect('welcome')
