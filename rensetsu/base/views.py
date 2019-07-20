from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *
from toshokan.models import Kanji

from base.forms import KanjiGroupForm

import random


def index(request):
    """ whatever should be seen by landing, generic user """

    display_kanji = Kanji.objects.filter(grade=2)
    possible_indices = Kanji.objects.values_list('id', flat=True)
    random_kanji_index = random.choice(possible_indices)
    kanji = Kanji.objects.get(id=random_kanji_index)

    truncated_meaning = ','.join(((((kanji.on_meaning.split(";"))[0]).split(','))[0:3]))

    context = {'kanji': kanji, 'truncated_meaning': truncated_meaning}
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

    # should return some 403s here based on user
    # comment this out if you don't want automatic group replacement
    # group.reviews.all().delete()
    
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

            # pre-select the kanji for no duplicates
            # note naive protection for small groups 
            if group_size == 0:
                return HttpResponseNotFound()
            elif group_size == 1:
                option_number = 1
            elif group_size == 2:
                option_number = 2
            else:
                pass

            restricted_kanji_set = group.group_kanji.exclude(character=kanji.character)
            distinct_kanji = random.sample(list(restricted_kanji_set), option_number-1)

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

                    random_distinct_kanji = distinct_kanji[count-1]
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

        # if review has been completed, delete group and start again
        if review.is_complete:
            # eventually this should be gatekept by another flag
            # that determines if review has been reviewed or not
            group.reviews.all().delete()
            return redirect('base:review_view', group_id)
        else:
            return redirect('base:review_process', review.id)

@login_required
def review_process(request, review_id):
    """ where the user is taken when a review exists """

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

    # mark that question has been answered
    review_object.is_complete = True
    review_object.save()

    # mark which option was chosen
    option.response_chosen = True
    option.save()

    # check if the whole quiz is complete
    responses = list(KanjiReviewObject.objects.filter(review__id=review_id).values_list('is_complete', flat=True))

    print(responses)
    
    if all(responses):
        review.is_complete = True
        review.save()

    data = {'correct': option.response_correct}

    return JsonResponse(data) 
