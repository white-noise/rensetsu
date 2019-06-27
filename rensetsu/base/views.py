from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .models import UserProfile, KanjiGroup
from toshokan.models import Kanji

from base.forms import KanjiGroupForm

def index(request):
    context = {}
    return render(request, 'base/index.html', context)

@login_required
def profile(request):
    userinfo = request.user.profile
    context  = {'userinfo': userinfo}
    return render(request, 'base/profile.html', context)

@login_required
def group(request):
    userinfo = request.user.profile
    context = {'form': KanjiGroupForm(), 'userinfo': userinfo}
    return render(request, 'base/group.html', context)

@login_required
def group_individual(request, group_id):
    userprofile = request.user.profile
    group   = get_object_or_404(KanjiGroup, pk=group_id)
    context = {'group': group}

    # forbidding users from seeing each-other's groups
    if not (group.user.id == userprofile.id):
        return HttpResponseNotFound()
    else:
        return render(request, 'base/group_individual.html', context)

@login_required
def add_group(request):
    userinfo = request.user.profile

    if request.method == 'POST':
        form = KanjiGroupForm(request.POST)
        new_group       = form.save(commit=False)
        new_group.user  = userinfo
        new_group.save()
        form.save_m2m()

    return redirect('base:profile')

@login_required
def delete_group(request, group_id):

    return redirect('base:index')

@login_required
def modify_group_name(request, group_id):

    return redirect('base:index')