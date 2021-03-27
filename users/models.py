from django.db import models

# Create your models here.

class Users(models.Model):
    name = 'users'
    id = models.CharField(max_length=100, primary_key=True)
    pw = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=50, null=True, blank=True, default='')

    def __str__(self):
        return 'id : ' + self.id + ', pw : ' + self.pw

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저들'

        db_table = 'users'