from django import forms
#from django.utils.translation import ugettext_lazy as _
import models

class PartyConfirmationForm(forms.ModelForm):
    #does not work. dunno why
    #def clean_adults(self):
        #pass
        #adults = self.cleaned_data['adults']
        #if(adults <= 0):
        #    raise forms.ValidationError(_('At least one adult required.'))
    class Meta:
        model = models.PartyConfirmation
        exclude= ('date_confirmed', 'hash_code')

        
