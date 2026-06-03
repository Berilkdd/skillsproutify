from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import JobRole
from .forms import JobRoleForm


@login_required
def welcome(request):
    print(request.user)
    print(request.user.is_authenticated)

    roles = JobRole.objects.filter(user=request.user)
    form = JobRoleForm()
    
    if request.method == "POST":

        title_data = request.POST.get('title')

        if title_data:
            job_role = JobRole(user=request.user, title=title_data)
            job_role.save()
            return redirect('selected_roles')          
    return render(
        request,
        "learning/welcome.html",
        {"roles": roles, "form": form}
    )

@login_required
def selected_roles(request):
    roles = JobRole.objects.filter(user=request.user)  
    form = JobRoleForm()            

    if request.method == "POST":
        new_job_role = JobRole(user=request.user)
        form = JobRoleForm(request.POST, instance=new_job_role)
        
        if form.is_valid():
            form.save() 
            return redirect('selected_roles')   
            
    return render(
        request, 
        "learning/selected_roles.html", 
        {"roles": roles, "form": form}
    )


    