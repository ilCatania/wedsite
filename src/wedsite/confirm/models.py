from django.db import models
from django.utils.translation import ugettext_lazy as _

class PartyConfirmation(models.Model):
    date_confirmed = models.DateTimeField(auto_now=True)
    hash_code = models.PositiveIntegerField()
    name = models.CharField(max_length=50, name=_("Name"), verbose_name=_('Full name'))
    adults = models.PositiveIntegerField(verbose_name=_("No. of adults"))
    children = models.PositiveIntegerField(verbose_name=_("No. of children (age 12 or lower)"), blank=True, null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('-date_confirmed',)
    def save(self):
        self.hash_code = hash((self.name, self.adults, self.date_confirmed))
        super(PartyConfirmation, self).save()
