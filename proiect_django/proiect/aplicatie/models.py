from django.db import models
from django.utils import timezone

class Autor(models.Model):
    nume = models.CharField(max_length = 63)
    email = models.EmailField(max_length = 63)

    def __str__(self):
        return self.nume

    def __repr__(self):
        return self.nume

class Articol(models.Model):
    titlu = models.CharField(max_length = 63)
    continut_articol = models.TextField()
    data_adaugarii = models.DateTimeField(default = timezone.now)
    autor = models.ForeignKey(Autor, on_delete = models.PROTECT)
    imagine = models.ImageField(upload_to='articol/%Y/%m/%d', default= 'static/aplicatie/default_img.jpg')
    def __str__(self):
        return self.titlu

    def __repr__(self):
        return self.titlu







