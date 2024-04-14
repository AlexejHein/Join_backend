from django.db import models


class MyModel(models.Model):
    _my_field = models.CharField(max_length=100)

    @property
    def my_field(self):
        return self._my_field

    @my_field.setter
    def my_field(self, value):
        self._my_field = value
