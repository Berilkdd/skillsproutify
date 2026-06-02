from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from learning.models import JobRole

def home(request):
    return render(request, 'home.html')

@login_required
def login_redirect(request):
    # From email confirmation link
    # The note confirms account has confirmed from mail link      
    # This if block customized with guidance from Google Ai
    if request.session.get('account_email_confirmed'):
        # Session information has to be cleared to prevent existing user to come here
        # so this part is only for a new user comes from sign-in page and email confirmation
        request.session.pop('account_email_confirmed', None)
        request.session.pop('account_user', None)       
        return redirect('/learning/welcome/')
    # From log-in page
    if request.user.jobrole_set.exists():
        # If they alredy have some roles selected
        return redirect('selected_roles')
    # If they haven't got any role yet
    return redirect('first_role')