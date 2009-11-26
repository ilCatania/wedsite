'''
Created on 03/ott/2009

@author: Gabriele
'''
from django import template
register = template.Library()


@register.inclusion_tag('mainnav.djhtml', takes_context=True)
def mainnav(context):
    return context
@register.inclusion_tag('subnav.djhtml', takes_context=True)
def subnav(context):
    return context


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.filter_function
def subnav_template(request):
    import re
    found = re.findall(r'^/?\w+/', request.path)
    if found:
        section = found[0][1:]
    else:
        section = 'home/'
    return section + 'subnav.djhtml'
    