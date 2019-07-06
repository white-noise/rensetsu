from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .models import Kanji
from base.models import KanjiGroup, KanjiComment
from base.forms import KanjiCommentForm

from django.utils import timezone

@login_required
def index(request):
    """ placeholder list of all kanji (eventually searchable) """
    kanji_list = Kanji.objects.all().order_by('grade')
    context    = {'kanji_list': kanji_list}
    
    return render(request, 'toshokan/index.html', context)

@login_required
def individual(request, kanji_id):
    """ main view for individual kanji """
    kanji          = get_object_or_404(Kanji, pk=kanji_id)
    userprofile    = request.user.profile

    reading_eng    = (kanji.reading_eng).split(",")
    reading_jpn    = (kanji.reading_jpn).split(",")
    # order comments with newest at the top
    comments       = kanji.kanji_comment.filter(user__id=userprofile.id).order_by('-date_time')
    groups         = kanji.kanjigroupelement_set.filter(group__user__id=userprofile.id)
    # check whether kanji is marked by three main properties
    is_interesting = kanji.interesting_kanji.filter(pk=userprofile.pk).exists()
    is_difficult   = kanji.difficult_kanji.filter(pk=userprofile.pk).exists()
    is_known       = kanji.known_kanji.filter(pk=userprofile.pk).exists()
    # order kanji compounds by most common first
    jukugo         = kanji.constituent_kanji.order_by('-frequency')

    context = {'kanji': kanji,
     'reading_eng': reading_eng,
     'reading_jpn': reading_jpn,
     'is_interesting': is_interesting,
     'is_difficult': is_difficult,
     'is_known': is_known,
     'comments': comments,
     'groups': groups,
     'jukugo': jukugo,
     }

    return render(request, 'toshokan/individual.html', context)

@login_required
def toggle_interesting(request, kanji_id):
    """ toggle kanji state for given user """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    userprofile = request.user.profile

    if request.method == 'POST':

        if kanji.interesting_kanji.filter(pk=userprofile.pk).exists():
            kanji.interesting_kanji.remove(userprofile)
        else:
            kanji.interesting_kanji.add(userprofile)

    return redirect('toshokan:individual', kanji_id)

@login_required
def toggle_difficult(request, kanji_id):
    """ toggle kanji state for given user """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    userprofile = request.user.profile

    if request.method == 'POST':

        if kanji.difficult_kanji.filter(pk=userprofile.pk).exists():
            kanji.difficult_kanji.remove(userprofile)
        else:
            kanji.difficult_kanji.add(userprofile)

    return redirect('toshokan:individual', kanji_id)

@login_required
def toggle_known(request, kanji_id):
    """ toggle kanji state for given user """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    userprofile = request.user.profile

    if request.method == 'POST':

        if kanji.known_kanji.filter(pk=userprofile.pk).exists():
            kanji.known_kanji.remove(userprofile)
        else:
            kanji.known_kanji.add(userprofile)

    return redirect('toshokan:individual', kanji_id)

@login_required
def comment(request, kanji_id):
    """ view for writing comment given kanji """
    kanji = get_object_or_404(Kanji, pk=kanji_id)

    context = {'kanji': kanji, 'form': KanjiCommentForm(),}

    return render(request, 'toshokan/comment.html', context)

@login_required
def add_comment(request, kanji_id):
    """ create a new comment object given kanji id """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    
    if request.method == 'POST':
        
        form = KanjiCommentForm(request.POST)
        
        if form.is_valid():
            new_comment       = form.save(commit=False)
            new_comment.kanji = kanji
            new_comment.user  = request.user.profile
            new_comment.save()
            form.save_m2m()
        else:

            context = {'kanji': kanji, 'form': KanjiCommentForm(),}
            return render(request, 'toshokan/comment.html', context)

    return redirect('toshokan:individual', kanji_id)

@login_required
def delete_comment(request, kanji_id, comment_id):
    """ remove a comment based on its id """
    comment = get_object_or_404(KanjiComment, pk=comment_id)
    userprofile = request.user.profile
    
    if request.method == 'POST':
        # check if comment poster is current user
        if comment.user == userprofile:  
            comment.delete()
        else:
            return HttpResponseNotFound()

    return redirect('toshokan:individual', kanji_id)

@login_required
def edit_comment(request, kanji_id, comment_id):
    """ view for editing comment belonging to current user """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    comment = get_object_or_404(KanjiComment, pk=comment_id)
    userprofile = request.user.profile
    form = KanjiCommentForm(initial={'comment': comment.comment})
    
    context = {'kanji': kanji, 'comment': comment, 'form': form,}

    if comment.user == userprofile:  
        return render(request, 'toshokan/edit_comment.html', context)
    else:
        return HttpResponseNotFound()

@login_required
def modify_comment(request, kanji_id, comment_id):
    """ edit comment belonging to current user """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    comment = get_object_or_404(KanjiComment, pk=comment_id)
    userprofile = request.user.profile
    
    if request.method == 'POST':
        
        form = KanjiCommentForm(request.POST)

        if form.is_valid():
            if comment.user == userprofile:
                comment.comment = form.cleaned_data['comment']
                comment.date_time = timezone.now()
                comment.save()
            else:
                return HttpResponseNotFound()
        else:
            context = {'kanji': kanji, 'comment': comment, 'form': form,}
            return render(request, 'toshokan/edit_comment.html', context)

    return redirect('toshokan:individual', kanji_id)

@login_required
def kanji_group_view(request, kanji_id):
    """ view for all groups kanji is in for curren user """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    userprofile = request.user.profile
    context = {'kanji': kanji, 'userprofile': userprofile}

    return render(request, 'toshokan/group_view.html', context)

@login_required
def kanji_delete_group_view(request, kanji_id):
    """ view for all groups from which kanji can be removed """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    userprofile = request.user.profile
    groups  = kanji.kanjigroupelement_set.filter(group__user__id=userprofile.id)
    context = {'kanji': kanji, 'userprofile': userprofile, 'groups': groups}

    return render(request, 'toshokan/delete_group.html', context)

@login_required
def add_kanji_to_group(request, kanji_id, group_id):
    """ add kanji with given id to given group """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile
    
    if request.method == 'POST':
        
        if group.user == userprofile:
            kanji.group_kanji.add(group)
        else:
            return HttpResponseNotFound()

    return redirect('toshokan:individual', kanji_id)

@login_required
def remove_kanji_from_group(request, kanji_id, group_id):
    """ remove kanji with given id from given group """
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile
    
    if request.method == 'POST':
        
        if group.user == userprofile:  
            if kanji.group_kanji.filter(id=group.id).exists():
                kanji.group_kanji.remove(group)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
    
    return redirect('toshokan:individual', kanji_id)