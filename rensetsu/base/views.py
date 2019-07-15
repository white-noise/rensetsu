from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import UserProfile, KanjiGroup
from toshokan.models import Kanji

from base.forms import KanjiGroupForm

import random


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
def modify_group_name_view(request, group_id):
    """ view for modifying a group name """
    group = get_object_or_404(KanjiGroup, pk=group_id)
    context = {'group': group, 'form': KanjiGroupForm(initial={'name': group.name})}
    
    return render(request, 'base/modify_group.html', context)

@login_required
def modify_group_name_submit(request, group_id):
    """ modify group name for current user given group """

    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile

    if request.method == 'POST':
        
        form = KanjiGroupForm(request.POST)
        
        if form.is_valid():
            if group.user == userprofile:
                name = form.cleaned_data['name']
                group.name = name
                group.save()
            else:
                return HttpResponseNotFound()
        else:
            context = {'group': group, 'form': form}
            return render(request, 'base/modify_group.html', context)

    return redirect('base:group_individual', group.id)

@login_required
def button_submit(request):
    """ test ajax function call """
    character = request.GET.get('character', None)
    data = {
        'is_kanji': Kanji.objects.filter(character=character).exists()
    }
    return JsonResponse(data)

@login_required
def group_review(request, group_id):
    """ show multiple choice kanji quiz groups """

    """ one concept is to use this to create a review
    object, and then send the user to the first page of that
    review object. then deal with garbage collection, as we
    want one quiz per group at all times? so a session, and
    then a score for each user corresponding to each kanji?
    """

    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile

    ordered_group = group.group_kanji.order_by('strokes')
    group_size = group.group_kanji.count()

    questions = []
    max_option_number = 3
    option_number = min([max_option_number, group_size])
    count = 0

    for kanji in ordered_group:

        option_indices = set(range(0, group_size))
        option_indices.remove(count)
        option_indices = list(option_indices)
        option_choices = random.sample(option_indices, option_number)

        correct_meaning = ','.join(((((kanji.on_meaning.split(";"))[0]).split(','))[0:3]))
        correct_option = {'option': correct_meaning, 'result': True}
        
        wrong_options = []
        for index in option_choices:
            wrong_meaning = ','.join((((ordered_group[index].on_meaning.split(";"))[0]).split(','))[0:3])
            wrong_options.append({'option': wrong_meaning})

        options = wrong_options
        options.append(correct_option)
        random.shuffle(options)
        
        question = {'kanji': kanji, 'options': options}
        questions.append(question)

        count = count + 1
    

    context = {
                'ordered_group': ordered_group, 
                'questions': questions
                }
    
    return render(request, 'base/review.html', context)

