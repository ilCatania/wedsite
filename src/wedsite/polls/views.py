import models
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from wedsite.ipsecurity.decorators import limit_daily_actions

POLLS_VOTED_COOKIE ='polls_voted'
SEPARATOR = '^$^'

def get_voted_poll_slugs(request):
    if(POLLS_VOTED_COOKIE in request.COOKIES):
        return  request.COOKIES[POLLS_VOTED_COOKIE].split(SEPARATOR)
    return []

def add_voted_poll_cookie(slug, request, response):
    voted_polls = get_voted_poll_slugs(request)
    voted_polls.append(slug)
    response.set_cookie(POLLS_VOTED_COOKIE, 
                        SEPARATOR.join(voted_polls),
                        max_age=60 * 60 * 24 * 60) #two months
    return response

def already_voted(request, slug):
    if slug in get_voted_poll_slugs(request):
        return True
    if 'REMOTE_ADDR' in request.META and request.META['REMOTE_ADDR']:
        ip_addr = request.META['REMOTE_ADDR']
        if ip_addr:
            return models.LoggedVote.objects.filter(ip_addr=ip_addr, slug=slug).count() > 0
    return False

def show_form_ajax(request, slug):
    if(already_voted(request, slug)):
        return show_results_ajax(request, slug, True)
    try:
        poll = models.Poll.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return build_poll_not_found_ajax(slug)
    if(hasattr(poll, 'singlechoicepoll')):
        template = 'polls/ajax_form_singlechoice.djhtml'
    elif(hasattr(poll, 'percentagepoll')):
        template = 'polls/ajax_form_percentage.djhtml'
    return render_to_response(template, 
                              {'poll': poll},
                              context_instance=RequestContext(request))

def show_results_ajax(request, slug, already_voted=False):
    try:
        poll = models.Poll.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return build_poll_not_found_ajax(slug)
    return build_results_ajax(request, poll, already_voted)

@limit_daily_actions
def vote_ajax(request, slug):
    if(already_voted(request, slug)):
        return show_results_ajax(request, slug, True)
    try:
        poll = models.Poll.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return build_poll_not_found_ajax(slug)
    if(request.method == 'POST' and 'voted' in request.POST):
        voted = int(request.POST['voted'])
    else:
        return build_results_ajax(request, poll)
    if(hasattr(poll, 'singlechoicepoll')):
        try:
            answer = poll.singlechoicepoll.choice_set.get(order=voted)
        except ObjectDoesNotExist:
            return build_answer_not_found_ajax(slug, voted)
    elif(hasattr(poll, 'percentagepoll')):
        try:
            answer = poll.percentagepoll.choice_set.get(perc=voted)
        except ObjectDoesNotExist:
            if(voted >= 0 and voted <= 100):
                answer = models.Percentage(perc = voted, parent=answer, poll=poll.percentagepoll)
                answer.votes = 0
            else:
                return build_answer_not_found_ajax(slug, voted)

    #if he made it here, he can vote
    if 'REMOTE_ADDR' in request.META and request.META['REMOTE_ADDR']:
        ip_addr = request.META['REMOTE_ADDR']
        if ip_addr:
            lv = models.LoggedVote(ip_addr=ip_addr, slug=slug, voted=answer.id)
            lv.save()

    answer.votes +=1
    answer.save(user=request.user)
    response = build_results_ajax(request, poll)
    return add_voted_poll_cookie(slug, request, response)

def build_results_ajax(request, poll, already_voted=False):
    if(hasattr(poll, 'singlechoicepoll')):
        template = 'polls/ajax_results_singlechoice.djhtml'
        data = []
        max_votes = 0
        tot_votes = 0;
        for choice in poll.singlechoicepoll.choice_set.all():
            data.append({'choice': choice.choice,
                         'votes': choice.votes,
                         'perc' : choice.votes,
                         'perc_width' : choice.votes,
                         'votedByG' : poll.votedByG == choice.order,
                         'votedByC' : poll.votedByC == choice.order,
                         })
            tot_votes += choice.votes
            if(max_votes < choice.votes):
                max_votes = choice.votes
        if(tot_votes):
            for d in data:
                d['perc'] *= 100 
                d['perc'] /= tot_votes
        if(max_votes):
            for d in data:
                d['perc_width'] *= 100
                d['perc_width'] /= max_votes
            
    elif(hasattr(poll, 'percentagepoll')):
        #todo: populate results
        template = 'polls/ajax_results_percentage.djhtml'
    return render_to_response(template,
                              {'data': data, 'already_voted': already_voted},
                              context_instance=RequestContext(request))

def build_poll_not_found_ajax(slug):
    return HttpResponse(_(u'Poll with slug %s not found.') % slug);

def build_answer_not_found_ajax(slug, voted):
    return HttpResponse(_(u'Poll with slug %(slug)s has no answer number %(number)d.') % {'slug': slug, 'number': voted});
