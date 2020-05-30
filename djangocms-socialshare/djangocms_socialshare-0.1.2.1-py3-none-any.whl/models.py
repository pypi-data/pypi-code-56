from cms.models.pluginmodel import CMSPlugin
from django.db import models
from enumfields import Enum
from enumfields import EnumField


class Type(Enum):
    FACEBOOK = 'facebook'
    # TWITTER = 'twitter'
    LINKEDIN = 'linkedin'
    EMAIL = 'email'
    GITHUB = 'github'


class Alignment(Enum):
    CENTER = 'center'
    LEFT = 'left'
    RIGHT = 'right'


class SocialItemAbstract(models.Model):
    type = EnumField(Type, default=None, max_length=32, blank=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True
        ordering = ['order']

    def get_icon_css_class(self) -> str:
        if self.type == Type.FACEBOOK:
            return 'fab fa-facebook-f'
        elif self.type == Type.LINKEDIN:
            return 'fab fa-linkedin-in'
        elif self.type == Type.EMAIL:
            return 'fas fa-envelope'
        elif self.type == Type.GITHUB:
            return 'fab fa-github'
        else:
            raise ValueError()

    def __str__(self) -> str:
        return ""


class SocialShareButton(SocialItemAbstract):
    plugin = models.ForeignKey(
        'SocialSharePluginModel',
        on_delete=models.CASCADE,
        related_name='items',
    )
    
    class Meta(SocialItemAbstract.Meta):
        abstract = False


class SocialLink(SocialItemAbstract):
    plugin = models.ForeignKey(
        'SocialLinksPluginModel',
        on_delete=models.CASCADE,
        related_name='items',
    )
    url = models.URLField()

    class Meta(SocialItemAbstract.Meta):
        abstract = False


class SocialPluginModelAbstract(CMSPlugin):
    alignment = EnumField(Alignment, default=Alignment.LEFT, max_length=32)
    size = models.IntegerField(default=25, help_text="In pixels")

    class Meta:
        abstract = True

    def copy_relations(self, old_instance: 'SocialSharePluginModel'):
        for items in old_instance.items.all():
            items.pk = None
            items.plugin = self
            items.save()

    def __str__(self):
        return ""


class SocialSharePluginModel(SocialPluginModelAbstract):
    pass


class SocialLinksPluginModel(SocialPluginModelAbstract):
    pass
