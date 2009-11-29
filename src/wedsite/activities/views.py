from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import models

def todo_list(request, template, slug):
    if not slug: raise Http404
    try:
        todo_list = models.TodoList.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
    return render_to_response(template,
                              {'list_description': todo_list.description,
                               'list_items': todo_list.todoitem_set.all() },
                              context_instance=RequestContext(request))
