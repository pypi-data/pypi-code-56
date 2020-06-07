from django.db import models

# Create your models here.


class User(models.Model):
    rootid = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    money=models.IntegerField(max_length=20)
    isdelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    setTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'User'

class Keys(models.Model):
    rootid = models.CharField(max_length=20)
    mykey=models.CharField(max_length=20)
    isdelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    setTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Keys'