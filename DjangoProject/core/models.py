from django.db import models

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    language = models.CharField(default='unknown', max_length=100)
    executable = models.BooleanField(default=False)
    owner = models.CharField(max_length=100)

    class Meta:
        ordering = ['created']
