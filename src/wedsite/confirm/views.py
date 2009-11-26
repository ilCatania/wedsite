'''
Created on 03/ott/2009

@author: Gabriele
'''
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
try:
    import json
except ImportError:
    from django.utils import simplejson as json #pre-2.6 fallback
import models
import forms
from wedsite.ipsecurity.decorators import limit_daily_actions

SEPARATOR = '$'
CONFIRMATIONS_COOKIE_NAME = 'saved_confirmations'
EDIT_ACTION = 'edit'
CREATE_ACTION = 'create'
NEW_ACTION = 'new'
UPDATE_ACTION = 'update'
DELETE_ACTION = 'delete'
EDIT_ID_ATTR = 'edit_confirmation_id'
MAX_CONFIRMATIONS = 3


def get_confirmation_hash_codes(request):
    hash_codes = []
    if CONFIRMATIONS_COOKIE_NAME in request.COOKIES and request.COOKIES[CONFIRMATIONS_COOKIE_NAME]:
        for hash_str in request.COOKIES[CONFIRMATIONS_COOKIE_NAME].split(SEPARATOR):
            try:
                hash_codes.append(int(hash_str))
            except ValueError:
                pass
    return hash_codes

def update_client_confirmations(response=HttpResponse(''), hash_codes=[]):
    response.set_cookie(CONFIRMATIONS_COOKIE_NAME, 
                        SEPARATOR.join([str(hash_code) for hash_code in hash_codes]),
                        max_age=60 * 60 * 24 * 60) #two months
    return response

def make_response(request, form_data=None, confirmations=None, errors=None, show_form=None):
    if show_form is None: show_form = form_data or not confirmations
    return render_to_response('wedding/party.djhtml',
                              {'content_class': 'party',
                               'confirmations': confirmations,
                               'errors': errors,
                               'showform' : show_form,
                               'can_add_more': confirmations and len(confirmations) < MAX_CONFIRMATIONS,
                               'prepopulated_data': form_data, 
                               },
                              context_instance=RequestContext(request))

@limit_daily_actions
def confirm(request):
    if request.method == 'POST' and NEW_ACTION in request.POST:
        return make_response(request)
        
    hash_codes = get_confirmation_hash_codes(request)
    if not hash_codes: return make_response(request)

    saved_confirmations = models.PartyConfirmation.objects.filter(hash_code__in=hash_codes)

    if request.method == 'POST':
        obj = None
        errors = {}
        if EDIT_ID_ATTR in request.POST and request.POST[EDIT_ID_ATTR]:
            id_str = request.POST[EDIT_ID_ATTR]
            try: obj = saved_confirmations.get(id = int(id_str))
            except ObjectDoesNotExist:
                errors = {'id': _('Requested object does not exist.')} #should never happen
            except ValueError:
                errors = {'id': _('Invalid id value: %s') % id_str }
            if DELETE_ACTION in request.POST:
                if errors: resp_data = {'success': False, 'message': errors['id'] }
                else: 
                    try: obj.delete()
                    except Exception, e:
                        resp_data = {'success': False, 'message': _('Unable to delete: %s') % e.message }
                    else:
                        to_remove = obj.hash_code
                        hash_codes.remove(to_remove)
                        resp_data = {'success': True, 'message': _(u"Confirmation deleted successfully!")}
                return update_client_confirmations(HttpResponse(json.dumps(resp_data)), 
                                                   hash_codes)
        else:
            obj = models.PartyConfirmation()
        if errors:
            show_form = UPDATE_ACTION in request.POST or CREATE_ACTION in request.POST
            return make_response(request, errors, confirmations=saved_confirmations, show_form=show_form)
        if EDIT_ACTION in request.POST :
            return make_response(request, form_data=obj.__dict__)
        if (CREATE_ACTION in request.POST and saved_confirmations.count() < MAX_CONFIRMATIONS) \
            or UPDATE_ACTION in request.POST:
            if obj.hash_code and obj.hash_code in hash_codes:
                hash_codes.remove(obj.hash_code) #need to remove, a new one will be created
            f = forms.PartyConfirmationForm(request.POST, instance = obj)
            if f.is_valid():
                f.save()
                saved_confirmations = list(saved_confirmations)
                saved_confirmations.append(obj)
                hash_codes.append(obj.hash_code)
                resp = make_response(request, confirmations=saved_confirmations)
                return update_client_confirmations(resp, hash_codes)
            else:
                return make_response(request, form_data=request.POST, errors=f.errors)

    return make_response(request, confirmations=saved_confirmations)

