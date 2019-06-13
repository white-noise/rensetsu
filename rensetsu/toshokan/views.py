from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Kanji

def index(request):
    kanji_list = Kanji.objects.all().order_by('grade')
    context = {'kanji_list': kanji_list}
    return render(request, 'toshokan/index.html', context)

def individual(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    return render(request, 'toshokan/individual.html', {'kanji': kanji})

@login_required
def profile(request):
    userinfo = request.user.profile
    context = {'userinfo': userinfo}
    return render(request, 'toshokan/profile.html', context)
