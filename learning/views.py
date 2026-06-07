from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from .models import JobRole, Resource
from .forms import JobRoleForm, ResourceForm 


@login_required
def welcome(request):
    print(request.user)
    print(request.user.is_authenticated)

    is_from_email = request.session.get('is_from_email', False)

    roles = JobRole.objects.filter(user=request.user)
    form = JobRoleForm()
    
    if request.method == "POST":

        title_data = request.POST.get('title')

        if title_data:
            job_role = JobRole(user=request.user, title=title_data)
            job_role.save()
            return redirect('selected_roles')        
    response = render(
        request,
        "learning/welcome.html",
        {"roles": roles, "form": form, "is_from_email": is_from_email}
    )
    if 'is_from_email' in request.session:
        del request.session['is_from_email']
    return response

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
def role_resources(request, role_id):
    job_role = get_object_or_404(JobRole, id=role_id, user=request.user)
    
    if not job_role.resource_set.exists():
        Resource.objects.create(job_role=job_role, name='Tools')
        Resource.objects.create(job_role=job_role, name='Courses')
        Resource.objects.create(job_role=job_role, name='Books')
        
    resources = job_role.resource_set.all()  
    form = ResourceForm()            

    if request.method == "POST":
        new_resource = Resource(job_role=job_role)
        form = ResourceForm(request.POST, instance=new_resource)
        
        if form.is_valid():
            form.save() 
            return redirect('role_resources', role_id=job_role.id)   
            
    return render(
        request, 
        "learning/resources.html", 
        {"job_role": job_role, "resources": resources, "form": form}
    )

@login_required
def delete_item(request, item_type, item_id):
    if item_type == 'role':
        item = get_object_or_404(JobRole, id=item_id, user=request.user)
        redirect_target = '/login-redirect/'  
    elif item_type == 'resource':
        item = get_object_or_404(Resource, id=item_id, job_role__user=request.user)        
        redirect_target = f'/learning/roles/{item.job_role.id}/resources/'
   
    if request.method == "POST":
        item.delete()
        
    return redirect(redirect_target)


@receiver(email_confirmed)
def set_email_verified_session(request, email_address, **kwargs):
        request.session['is_from_email'] = True

