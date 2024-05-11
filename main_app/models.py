from django.db import models

class todo(models.Model):
    title = models.CharField(max_length=1000)
    added = models.DateField(auto_now_add=True)
    due = models.DateField()
    status = models.IntegerField()
