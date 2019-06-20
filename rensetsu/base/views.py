from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from toshokan.models import Kanji

def index(request):
    context = {}
    return render(request, 'base/index.html', context)

@login_required
def profile(request):
    userinfo = request.user.profile
    context = {'userinfo': userinfo}
    return render(request, 'base/profile.html', context)