from django.shortcuts import render, redirect
from .models import JobRole
from .forms import JobRoleForm

def first_role(request):
    return render(request, "learning/first_role.html")

def welcome(request):
    print(request.user)
    print(request.user.is_authenticated)

    roles = JobRole.objects.filter(user=request.user)
    form = JobRoleForm()
    
    if request.method == "POST":
        form = JobRoleForm(request.POST)
        if form.is_valid():
            job_role = form.save(commit=False)
            job_role.user = request.user
            job_role.save()
            return redirect('selected_roles')          
    return render(
        request,
        "learning/welcome.html",
        {"roles": roles, "form": form}
    )

def selected_roles(request):
    roles = JobRole.objects.filter(user=request.user)  
    form = JobRoleForm()            

    if request.method == "POST":
        form = JobRoleForm(request.POST)
        if form.is_valid():
            job_role = form.save(commit=False)
            job_role.user = request.user
            job_role.save()
            return redirect('selected_roles')   
    return render(
        request, 
        "learning/roles.html", 
        {"roles": roles, "form": form}
    )


    