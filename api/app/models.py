from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model


USER = get_user_model()

class Post(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    body = models.TextField(_("Body"))
    author = models.ForeignKey(to=USER, verbose_name=_("Author"), on_delete=models.CASCADE)
    created_date = models.DateTimeField(_("Created date"), default=timezone.now)
    published_date = models.DateTimeField(_("Published_date"), default=None, blank=True, null=True)
    is_published = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        ordering = ['-published_date']

    def publish(self):
        self.published_date = timezone.now()
        self.is_published = True
        self.save()
    
    def private(self):
        self.is_published = False
        self.save()

    def __str__(self) -> str:
        return "<Title: %s, Author: %s>" % (self.title, self.author)

