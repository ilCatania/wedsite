from models import get_sitemap

def mainnav(request):
    sitemap = get_sitemap()
    for ent in sitemap: ent['selected'] = request.path.startswith(ent['url']) 
    return { 'mainnav': sitemap }

def subnav(request):
    sitemap = get_sitemap()
    for ent in sitemap:
        if request.path.startswith(ent['url']):
            children = ent['children']
            break
    else: children = []
    for ent in children: ent['selected'] = request.path.startswith(ent['url']) 
    return { 'subnav': children }
