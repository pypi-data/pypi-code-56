from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Create your models here.

class AccountModel(models.Model):
    pass

class AccountPropertyModel(models.Model):

    name = models.TextField(
        max_length=100
    )

    value = models.TextField(
        max_length=100
    )
    account = models.ForeignKey(
        default=None,
        null=True,
        blank=True,
        to=AccountModel,
        on_delete=models.CASCADE,
    )


class SnippetModel(models.Model):
    """
    Model for code snippets.
    """

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        verbose_name = _('Töredék')
        verbose_name_plural = _('Töredékek')
        ordering = ['created']
