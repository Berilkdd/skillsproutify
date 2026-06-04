from django.shortcuts import render, redirect, get_object_or_404
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


@login_required
def delete_job_role(request, role_id):
    """
    Kullanıcının seçtiği rolü güvenli bir şekilde siler.
    """
    # Sadece giriş yapmış kullanıcının kendi rolünü bul (Güvenlik zırhı)
    job_role = get_object_or_404(JobRole, id=role_id, user=request.user)
    
    if request.method == "POST":
        job_role.delete()
        
    # Rol silindikten sonra durum kontrolü için yönlendiriyoruz
    return redirect('/login-redirect/')