from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *
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
def review_view(request, group_id):
    """ creation and redirect to new review """
    group = get_object_or_404(KanjiGroup, pk=group_id)
    userprofile = request.user.profile

    is_review = group.reviews.all().exists()
    group_size = group.group_kanji.count()
    max_option_number = 3
    option_number = min([max_option_number, group_size])

    if not is_review:
        # create new review
        new_review = KanjiReview(user=userprofile, group=group)
        new_review.save()

        # get kanji set from group
        kanji_set = group.group_kanji.all()

        # for each kanji, construct a blank review object
        for kanji in kanji_set:
            new_object = KanjiReviewObject(kanji=kanji, review=new_review)
            new_object.save()

            # for each object, create a list of answers
            for count in range(option_number):

                if count == 0:
                    # construct the proper answer 
                    correct_meaning = ','.join(((((kanji.on_meaning.split(";"))[0]).split(','))[0:3]))
                    # eventually delegate above to other function that takes a kanji 
                    # and spits out answers in dictionary
                    new_response = KanjiReviewObjectOption(
                            review_object=new_object,
                            possible_response=correct_meaning,
                            response_correct=True,
                            )
                    new_response.save()
                else:
                    # construct a plausible but wrong answer
                    restricted_kanji_set = group.group_kanji.exclude(character=kanji.character)

                    # note there is no protection for one-kanji groups
                    # in that case, one should populate from random selection
                    # of other kanji, or direct to error page
                    random_distinct_kanji = random.choice(restricted_kanji_set)
                    incorrect_meaning = ','.join(((((random_distinct_kanji.on_meaning.split(";"))[0]).split(','))[0:3]))

                    new_response = KanjiReviewObjectOption(
                                review_object=new_object,
                                possible_response=incorrect_meaning,
                                response_correct=False,
                                )
                    new_response.save()

        return redirect('base:review_process', new_review.id)

    else:
        
        # ideally there should only ever be one
        review = group.reviews.all().first()
        return redirect('base:review_process', review.id)

@login_required
def review_process(request, review_id):
    """ where the user is taken when a review exists """

    """ 
    within this function we will render the quiz, either all
    at once or step by step. each of the elements will in turn
    call another view via ajax (or fetch) that will silently mark
    the answer as correct or incorrect, and the question as marked
    or no (saved for display/deactivation on return)

    on submit, this should take us to a review page, which gives
    us a summary on the review, then deletes it, and redirects us
    home.

    there should also be a flag for whether a review is finished or
    not, which tells us when it should be deleted. add this to the model,
    maintaining concurrency, and display it on the link to the review
    """
    review = get_object_or_404(KanjiReview, pk=review_id)

    context = {"review": review}
    
    return render(request, 'base/review_view.html', context)

@login_required
def review_submit(request):

    review_id = request.GET.get('review_id', -1)
    object_id = request.GET.get('object_id', -1)
    option_id = request.GET.get('option_id', -1)

    review = get_object_or_404(KanjiReview, pk=review_id)
    review_object = get_object_or_404(KanjiReviewObject, pk=object_id)
    option = get_object_or_404(KanjiReviewObjectOption, pk=option_id)

    # return whether the answer was correct or not
    # as well as any other important metadata

    data = {'correct': option.response_correct}

    return JsonResponse(data) 
