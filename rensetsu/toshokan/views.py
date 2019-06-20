from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import AddUserForm
from .models import Kanji

@login_required
def index(request):
    kanji_list = Kanji.objects.all() # .order_by('strokes') # for example
    context = {'kanji_list': kanji_list}
    return render(request, 'toshokan/index.html', context)

@login_required
def individual(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    reading_eng = (kanji.reading_eng).split(",")
    reading_jpn = (kanji.reading_jpn).split(",")

    return render(request, 'toshokan/individual.html',
     {'kanji': kanji,
     'reading_eng': reading_eng,
     'reading_jpn': reading_jpn,
     'form': AddUserForm()
     })

@login_required
def add_user(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            kanji.interesting_kanji.add(form.cleaned_data['user'])
    return redirect('individual', kanji_id)