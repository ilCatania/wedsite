from django.db import models

class LoggedAction(models.Model):
    ip_addr= models.CharField(max_length=20, primary_key=True)
    last_action=models.DateTimeField(auto_now=True)
    action_count=models.PositiveIntegerField(default=0)
    banned=models.BooleanField(default=False) # to ban IPs manually
    class Meta:
        ordering = ('last_action', )
