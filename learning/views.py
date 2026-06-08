from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from .models import JobRole, Resource, ResourceItem
from .forms import JobRoleForm, ResourceForm, ResourceItemForm


@login_required
def welcome(request):
    """
    Renders the welcome page and handles the user's initial
    job role submission.
    """
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
    """
    Renders the selected roles dashboard and handles new job role creation.
    """
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


# Google ai help to prevent default resources from regenerating
# when the user intentionally clears the entire list.
@login_required
def role_resources(request, role_id):
    """
    Displays sub-categories for a role and seeds default tracks if empty.
    """
    job_role = get_object_or_404(JobRole, id=role_id, user=request.user)
    session_key = f'role_{job_role.id}_initialized'

    if (not job_role.resource_set.exists() and
            not request.session.get(session_key, False)):
        Resource.objects.create(job_role=job_role, name='Tools')
        Resource.objects.create(job_role=job_role, name='Courses')
        Resource.objects.create(job_role=job_role, name='Books')
        request.session[session_key] = True

    resources = job_role.resource_set.all()
    form = ResourceForm()

    if request.method == "POST":
        new_resource = Resource(job_role=job_role)
        form = ResourceForm(request.POST, instance=new_resource)

        if form.is_valid():
            form.save()
            request.session[session_key] = True
            return redirect('role_resources', role_id=job_role.id)

    return render(
        request,
        "learning/resources.html",
        {"job_role": job_role, "resources": resources, "form": form}
    )


@login_required
def resource_items(request, resource_id):
    """
    Renders tracking line-items for a category and handles new item creation.
    """
    resource = get_object_or_404(
        Resource, id=resource_id, job_role__user=request.user
    )
    items = resource.resourceitem_set.all()
    form = ResourceItemForm()

    if request.method == "POST":
        new_item = ResourceItem(resource=resource)
        form = ResourceItemForm(request.POST, instance=new_item)

        if form.is_valid():
            form.save()
            return redirect('resource_items', resource_id=resource.id)

    return render(
        request,
        "learning/resource_items.html",
        {"resource": resource, "items": items, "form": form}
    )


@login_required
def delete_item(request, item_type, item_id):
    """
    Handles secure database deletion for roles, resources,
    or individual line-items.
    """
    if item_type == 'role':
        item = get_object_or_404(JobRole, id=item_id, user=request.user)
        redirect_target = '/login-redirect/'
    elif item_type == 'resource':
        item = get_object_or_404(
            Resource, id=item_id, job_role__user=request.user
        )
        redirect_target = f'/learning/{item.job_role.id}/'
    elif item_type == 'resource_item':
        item = get_object_or_404(
            ResourceItem, id=item_id, resource__job_role__user=request.user
        )
        redirect_target = f'/learning/items/{item.resource.id}/'

    if request.method == "POST":
        item.delete()

    return redirect(redirect_target)


@login_required
def toggle_item_status(request, item_id):
    """
    Cycles a tracking item's status inline between planted,
    growing, and bloomed states.
    """
    item = get_object_or_404(
        ResourceItem, id=item_id, resource__job_role__user=request.user
    )

    if item.status == 'planted':
        item.status = 'growing'
    elif item.status == 'growing':
        item.status = 'bloomed'
    else:
        item.status = 'planted'

    item.save()
    return redirect('resource_items', resource_id=item.resource.id)


@receiver(email_confirmed)
def set_email_verified_session(request, email_address, **kwargs):
    request.session['is_from_email'] = True
