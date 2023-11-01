from django.db import models

# Create your models here.
class LegalQAFinal(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    law = models.CharField(max_length=200, null=True, blank=True)
    prec = models.CharField(max_length=200, null=True, blank=True)
    embedding = models.TextField(null=True, blank=True)