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
    userprofile = request.user.profile
    context  = {'userprofile': userprofile}
    return render(request, 'base/profile.html', context)

@login_required
def group(request):
    context = {'form': KanjiGroupForm()}
    return render(request, 'base/group.html', context)

@login_required
def group_individual(request, group_id):
    userprofile = request.user.profile
    group   = get_object_or_404(KanjiGroup, pk=group_id)
    context = {'group': group}

    if not (group.user.id == userprofile.id):
        return HttpResponseNotFound()
    else:
        return render(request, 'base/group_individual.html', context)

@login_required
def add_group(request):
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
def delete_group(request, group_id):

    return redirect('base:index')

@login_required
def modify_group_name(request, group_id):

    return redirect('base:index')