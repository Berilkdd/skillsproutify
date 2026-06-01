from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_redirect(request):
    user = request.user

    from_email_link = request.GET.get('from_email_link')

    if from_email_link:        
        return redirect('welcome')
    
    elif user.jobrole_set.exists():       
        return redirect('selected_roles')
    
    else:        
        return redirect('first_role')

def login_redirect(request):
    print(request.GET)