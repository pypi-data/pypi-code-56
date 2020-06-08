from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from nocton.tools.model_manip import in_objects, has_field
from nocton.account_validation.tools import validation_enable
from nocton.tools import print_f
from nocton.account_validation.backends import exe_backends

AUTH_MODEL = get_user_model()
ACCOUNT_VALIDATION = validation_enable()


class AccountValidatorToken(models.Model):
    user = models.OneToOneField(AUTH_MODEL, on_delete=models.CASCADE, related_name="activation_token")
    key = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        is_new = not in_objects(self, AccountValidatorToken)

        super().save(*args, **kwargs)
        
        if is_new:
            print_f("Objeto novo")
            self.deactive_user()



    def active_user(self):
        print_f("Habilitando usuário...")
        self.user = exe_backends(self.user, is_activating=True)
        self.user.save()


    def active_user(self):
        print_f("Habilitando usuário...")
        user = exe_backends(self.user, is_activating=True)

        assert(
            isinstance(user, AUTH_MODEL)
        ), "Os backends devem retornar um usuário"

        self.user = user
        self.user.save()


    def deactive_user(self):
        print_f("Desabilitando usuário...")
        user = exe_backends(self.user, is_activating=False)

        assert(
            isinstance(user, AUTH_MODEL)
        ), "Os backends devem retornar um usuário"

        self.user = user
        self.user.save()


@receiver(post_save, sender=AUTH_MODEL)
def create_validation_token(sender, instance=None, created=False, **kwargs):
    if created:
        if ACCOUNT_VALIDATION and not instance.is_superuser:
            validation_token = AccountValidatorToken.objects.create(user=instance)


#---------ACCOUNT----------
@receiver(pre_save, sender=AccountValidatorToken)
def create_key(sender, instance=None, **kwargs):
    if not in_objects(instance, AccountValidatorToken):
        instance.key = get_random_string(length=8)

@receiver(pre_delete, sender=AccountValidatorToken)
def delete(sender, instance=None, **kwargs):
    instance.active_user()