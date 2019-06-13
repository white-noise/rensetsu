from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, 'base/index.html', context)

@login_required
def profile(request):
    userinfo = request.user.profile
    context = {'userinfo': userinfo}
    return render(request, 'base/profile.html', context)