from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=32, blank=False, unique=True, verbose_name="name")
    logo = models.ImageField(verbose_name="logo")

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)
