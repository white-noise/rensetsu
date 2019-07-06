from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .models import UserProfile, KanjiGroup
from toshokan.models import Kanji

from base.forms import KanjiGroupForm

def index(request):
    """ whatever should be seen by landing, generic user """
    context = {}
    return render(request, 'base/index.html', context)

@login_required
def profile(request):
    """ user's main profile """
    userprofile = request.user.profile
    context  = {'userprofile': userprofile}
    return render(request, 'base/profile.html', context)

@login_required
def group(request):
    """ view for creating a new group """
    context = {'form': KanjiGroupForm()}
    return render(request, 'base/group.html', context)

@login_required
def group_individual(request, group_id):
    """ view for individual group for current user """
    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile
    context = {'group': group}

    if group.user.id == userprofile.id:
        return render(request, 'base/group_individual.html', context)  
    else:
        return HttpResponseNotFound()

@login_required
def add_group(request):
    """ add group for current user with given name """
    userprofile = request.user.profile

    if request.method == 'POST':
        
        form = KanjiGroupForm(request.POST)
        
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.user = userprofile
            new_group.save()
            form.save_m2m()
        else:
            context = {'form': form}
            return render(request, 'base/group.html', context)

    return redirect('base:profile')

@login_required
def delete_group_view(request):
    """ view for deleting a given group """
    groups = request.user.profile.group_profile.all()
    context = {'groups' : groups}

    return render(request, 'base/delete_group_view.html', context)

@login_required
def delete_group(request, group_id):
    """ delete group for current user with given name """
    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile

    if group.user.id == userprofile.id:   
        group.delete()  
    else:
        return HttpResponseNotFound()

    return redirect('base:profile')

@login_required
def modify_group_name(request, group_id):
    """ modify group name for current user given group """

    return redirect('base:profile')