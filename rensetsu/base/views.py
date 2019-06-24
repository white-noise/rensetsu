from django.shortcuts import render, redirect, get_object_or_404
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
    context = {'form': KanjiGroupForm()}
    return render(request, 'base/group.html', context)

@login_required
def group_individual(request, group_id):
    group_object   = get_object_or_404(KanjiGroup, pk=group_id)
    context = {'group': group_object}
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