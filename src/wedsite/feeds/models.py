from django.contrib.syndication.feeds import Feed
from wedsite.news.models import News

class LatestEntriesEn(Feed):
    title = "Cecilia & Gabriele: the wedding"
    link = "/home/news/"
    language = "en-us"
    description = "Cecilia and Gabriele are getting married! " + \
        "This feed will keep you posted about their progress and " + \
        "allow you to discover what's behind the scenes."
    def items(self):
        return News.objects.order_by('-pub_date')[:5]
    def item_link(self, item):
        return '/home/news/'+item.slug + '/'

class LatestEntriesIt(Feed):
    title = "Cecilia & Gabriele: il matrimonio"
    link = "/home/news/"
    language = "it-it"
    description = "Cecilia e Gabriele si sposano! " + \
        "Questo feed ti terra' aggiornato sui loro progressi e " + \
        "ti permettera' di scoprire cosa succede dietro le quinte."
    def items(self):
        return News.objects.order_by('-pub_date')[:5]
    def item_link(self, item):
        return '/home/news/'+item.slug + '/'
