from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.forms.fields import CharField


class history(models.Model):
    owner = models.CharField(max_length=233)
    orginal_txt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} - {self.orginal_text[:30]}"


