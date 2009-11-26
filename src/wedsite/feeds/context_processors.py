def feed_url(request):
    lang = 'it'
    try:
        lang = request.LANGUAGE_CODE.split('-')[0]
    except:
        pass
    #return {'feed_url': u'/feeds/latest-%s/' % lang}
    return {'feed_url': u'http://feeds.feedburner.com/cgwedding-%s' % lang}
