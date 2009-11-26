from django.db import models
import multilingual

class Poll(models.Model):
    slug   = models.SlugField(max_length=12)
    pub_date = models.DateTimeField()
    votedByG = models.PositiveIntegerField(default=0,null=True)
    votedByC = models.PositiveIntegerField(default=0,null=True)
    class Meta:
        #ordering = ('pub_date', 'slug')
        pass

class SingleChoicePoll(Poll):
    class Translation(multilingual.Translation):
        question = models.CharField(max_length=200)
    def __unicode__(self):
        return self.question

class PercentagePoll(Poll):
    class Translation(multilingual.Translation):
        question = models.CharField(max_length=200)
        min = models.CharField(max_length=200)
        low = models.CharField(max_length=200)
        avg = models.CharField(max_length=200)
        high = models.CharField(max_length=200)
        max = models.CharField(max_length=200)
    def __unicode__(self):
        return self.question
    def current_percentage(self):
        pass #todo

class Answer(models.Model):
    votes = models.PositiveIntegerField(default=0)
    def __unicode__(self):
            return u'%s votes' % self.votes
    class Meta:
        #ordering = ('poll__pub_date', 'votes')
        abstract = True
    def save(self, **kwargs):
        if('user' in kwargs):
            if(hasattr(self, 'choice')):
                self.choice.save(kwargs['user'])
            elif(hasattr(self, 'percentage')):
                self.percentage.save(kwargs['user'])
        else:
            return super(Answer, self).save()

class Choice(Answer):
    poll = models.ForeignKey(SingleChoicePoll)
    order = models.PositiveIntegerField()
    class Translation(multilingual.Translation):
        choice = models.CharField(max_length=200)
        def __unicode__(self):
            return self.choice
    class Meta:
        ordering = ('order',)
    def save(self, **kwargs):
        if 'user' in kwargs:
            user = kwargs['user']
            if(user.is_authenticated()):
                if(user.username == 'gabriele'):
                    self.poll.votedByG = self.order
                elif(user.username == 'cecilia'):
                    self.poll.votedByC = self.order
                self.poll.save()
        return super(Choice, self).save()

class Percentage(Answer):
    poll = models.ForeignKey(PercentagePoll)
    perc = models.PositiveIntegerField()
    def __unicode__(self):
        return self.perc
    def save(self, **kwargs):
        if 'user' in kwargs:
            user = kwargs['user']
            if(user.is_authenticated()):
                if(user.username == 'gabriele'):
                    self.poll.votedByG = self.perc
                elif(user.username == 'cecilia'):
                    self.poll.votedByC = self.perc
                self.poll.save()
        return super(Percentage, self).save()

class LoggedVote(models.Model):
    #still no support for multiple fields as pri key, so...
    ip_addr=models.CharField(max_length=20, db_index=True)
    slug=models.SlugField(max_length=12, db_index=True)
    voted=models.PositiveIntegerField(default=0,null=True)

