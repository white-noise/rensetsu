from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Kanji
from base.models import KanjiGroup
from base.forms import KanjiCommentForm

@login_required
def index(request):
    kanji_list = Kanji.objects.all() # .order_by('strokes') # for example
    context    = {'kanji_list': kanji_list}
    return render(request, 'toshokan/index.html', context)

@login_required
def individual(request, kanji_id):
    kanji          = get_object_or_404(Kanji, pk=kanji_id)
    userprofile    = request.user.profile

    reading_eng    = (kanji.reading_eng).split(",")
    reading_jpn    = (kanji.reading_jpn).split(",")
    comments       = kanji.kanji_comment.all().filter(user=request.user.profile)
    groups         = kanji.kanjigroupelement_set.all()
    is_interesting = kanji.interesting_kanji.all().filter(pk=userprofile.pk).exists()
    is_difficult   = kanji.difficult_kanji.all().filter(pk=userprofile.pk).exists()
    is_known       = kanji.known_kanji.all().filter(pk=userprofile.pk).exists()

    return render(request, 'toshokan/individual.html',
     {'kanji': kanji,
     'reading_eng': reading_eng,
     'reading_jpn': reading_jpn,
     'is_interesting': is_interesting,
     'is_difficult': is_difficult,
     'is_known': is_known,
     'comments': comments,
     'groups': groups,
     })

@login_required
def toggle_interesting(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    if request.method == 'POST':
        # big question is what to do if this is None
        # no idea what the break cases are
        userprofile = request.user.profile
        if kanji.interesting_kanji.all().filter(pk=userprofile.pk).exists():
            kanji.interesting_kanji.remove(userprofile)
        else:
            kanji.interesting_kanji.add(userprofile)
    return redirect('toshokan:individual', kanji_id)

@login_required
def toggle_difficult(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    if request.method == 'POST':
        userprofile = request.user.profile
        if kanji.difficult_kanji.all().filter(pk=userprofile.pk).exists():
            kanji.difficult_kanji.remove(userprofile)
        else:
            kanji.difficult_kanji.add(userprofile)
    return redirect('toshokan:individual', kanji_id)

@login_required
def toggle_known(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    if request.method == 'POST':
        userprofile = request.user.profile
        if kanji.known_kanji.all().filter(pk=userprofile.pk).exists():
            kanji.known_kanji.remove(userprofile)
        else:
            kanji.known_kanji.add(userprofile)
    return redirect('toshokan:individual', kanji_id)

@login_required
def comment(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    reading_eng = (kanji.reading_eng).split(",")
    reading_jpn = (kanji.reading_jpn).split(",")

    return render(request, 'toshokan/comment.html',
     {'kanji': kanji,
     'reading_eng': reading_eng,
     'reading_jpn': reading_jpn,
     'form': KanjiCommentForm(),
     })

@login_required
def add_comment(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    if request.method == 'POST':
        form = KanjiCommentForm(request.POST)
        new_comment       = form.save(commit=False)
        new_comment.kanji = kanji
        new_comment.user  = request.user.profile
        new_comment.save()
        form.save_m2m()

    return redirect('toshokan:individual', kanji_id)

@login_required
def kanji_group_view(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    userprofile = request.user.profile
    context = {'kanji': kanji, 'userprofile': userprofile}

    return render(request, 'toshokan/group_view.html', context)

@login_required
def add_kanji_to_group(request, kanji_id, group_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    group = get_object_or_404(KanjiGroup, pk=group_id)
    
    if request.method == 'POST':
        kanji.group_kanji.add(group)

    return redirect('toshokan:individual', kanji_id)