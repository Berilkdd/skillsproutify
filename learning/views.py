from django.shortcuts import render, redirect
from .models import JobRole
from .forms import JobRoleForm

def first_role(request):
    return render(request, "learning/first_role.html")


def selected_roles(request):
    roles = JobRole.objects.all()  
    form = JobRoleForm()            

    if request.method == "POST":
        form = JobRoleForm(data=request.POST)
        if JobRoleForm.is_valid():
            form.save()
            return redirect('selected_roles')  


    return render(request, "learning/selected_roles.html", 
                  {"roles": roles,
                   "form": form,}
    )