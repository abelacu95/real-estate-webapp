from django.db import models
import datetime, os
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import formats
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator
from fontawesome_5.fields import IconField

class City (models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Ciudades'

    def __str__(self):
        return self.title



######################################################

def get_image_path(instance, filename):
    return os.path.join('photos',filename)

class Service (models.Model):
    name = models.CharField(max_length=30)
    iconClass = IconField()

    class Meta:
        verbose_name_plural="Servicios"

    def __str__(self):
        return self.name

class Estate (models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    dailyRate = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to=get_image_path,blank=True, null=False)
    city = models.ForeignKey(City,on_delete=models.PROTECT, null=False)
    descripcion = models.TextField(max_length=500)
    pax = models.PositiveIntegerField(validators=[MaxValueValidator(7)])
    services = models.ManyToManyField(Service)

    class Meta:
        verbose_name_plural='Propiedades'

    def __str__(self):
        return self.title

######################################################
class Reservation (models.Model):
    code = models.CharField(max_length=30)
    total = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    user = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural='Reservaciones'
        ordering=('total','code')

    def __str__(self):
        return self.code

######################################################
class RentDate(models.Model):

    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, null=True, blank=True)
    estate = models.ForeignKey(Estate, on_delete=models.PROTECT, null=False,blank=False)
    dateFrom =  models.DateField(blank=True, null=True)
    dateTo =  models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural='Fechas de Alquiler'
        ordering=('dateFrom','dateTo','estate')

    def getDates(self):
        
        date_format = "%d-%m-%Y"
        a = datetime.strptime(self.dateFrom, date_format)
        b = datetime.strptime(self.dateTo, date_format)
        return b - a

    def __str__(self):
        return  "Del " + str(self.dateFrom.strftime("%d-%m-%Y")) + " hasta " + str(self.dateTo.strftime("%d-%m-%Y"))

