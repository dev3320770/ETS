from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.admin import AdminSite
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from datetime import datetime, timedelta

# Create your models here.
AdminSite.site_header = ('ETIMS Administration')


class Occupation(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sex (models.Model):
    class Meta:
        verbose_name = u'Sex'
        verbose_name_plural = u'Sex'

    name = models.CharField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TicketCategory (models.Model):
    class Meta:
        verbose_name = u'Ticket Category'
        verbose_name_plural = u'Ticket Categories'

    name = models.CharField(max_length=225)
    description = models.TextField(max_length=225, blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Severity (models.Model):
    class Meta:
        verbose_name = u'Severity'
        verbose_name_plural = u'Severities'

    name = models.CharField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EyesColor (models.Model):
    class Meta:
        verbose_name = u'Eye Color'
        verbose_name_plural = u'Eyes Color'

    name = models.CharField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HairColor (models.Model):
    class Meta:
        verbose_name = u'Hair Color'
        verbose_name_plural = u'Hair Color'

    name = models.CharField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ViolationCode (models.Model):
    class Meta:
        verbose_name = u'Violation Code'
        verbose_name_plural = u'Violation Codes'

    code = models.CharField(max_length=225)
    amount = models.FloatField()
    description = models.TextField(max_length=225)
    ticketCategory = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class LicenceCode (models.Model):
    class Meta:
        verbose_name = u'Licence Code'
        verbose_name_plural = u'Licence Codes'

    code = models.CharField(max_length=225)
    description = models.TextField(max_length=225, blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class DriverRestriction (models.Model):
    class Meta:
        verbose_name = u'Driver Restriction'
        verbose_name_plural = u'Driver Restrictions'

    code = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VehRestriction (models.Model):
    class Meta:
        verbose_name = u'Vehicle Restriction'
        verbose_name_plural = u'Vehicle Restrictions'

    code = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='static/photos/%Y/%m/%d/', null=False, blank=False, default='static/30x30.png', max_length=100)
    gender = models.ForeignKey(Sex, on_delete=models.CASCADE, null=True, blank=True)
    idNumber = models.CharField(max_length=12)
    cellNumber = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    town = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class LicenceInfo (models.Model):
    class Meta:
        verbose_name = u'Licence Information'
        verbose_name_plural = u'Licence Information'

    licenceNumber = models.CharField(max_length=225)
    licenceCode = models.ForeignKey(LicenceCode, on_delete=models.CASCADE)
    licenceBarcode = models.CharField(max_length=100)
    idNumber = models.CharField(max_length=12)
#    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    owner = models.CharField(max_length=12)
    driverRestriction = models.ManyToManyField(DriverRestriction)
    vehRestriction = models.ManyToManyField(VehRestriction)
    issuedBy = models.CharField(max_length=225)
    validityStart = models.DateField()
    validityEnd = models.DateField()
    firstIssue = models.DateField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.licenceNumber


class VehicleInfo (models.Model):
    class Meta:
        verbose_name = u'Vehicle Information'
        verbose_name_plural = u'Vehicles Information'

    regNumber = models.CharField(max_length=225)
    vinNumber = models.CharField(max_length=225)
    regBarcode = models.CharField(max_length=100)
#    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    owner = models.CharField(max_length=12)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.regNumber


class VehicleMake (models.Model):
    class Meta:
        verbose_name = u'Vehicle Make'
        verbose_name_plural = u'Vehicle Make'

    name = models.CharField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Direction (models.Model):
    name = models.CharField(max_length=225)
    dateCreated = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def get_deadline():
    return datetime.today() + timedelta(days=14)


class Ticket (models.Model):
    ticketCategory = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    cellNumber = models.CharField(max_length=225)
    email = models.EmailField()
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    idNumber = models.CharField(max_length=12, blank=True, null=True)
    vinNumber = models.CharField(max_length=225, blank=True, null=True)
    regNumber = models.CharField(max_length=225, blank=True, null=True)
    licenceBarcode = models.CharField(max_length=100, blank=True, null=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    locationLat = models.FloatField(blank=True, null=True)
    locationLog = models.FloatField(blank=True, null=True)
    locationAlt = models.FloatField(blank=True, null=True)
    direction = models.CharField(max_length=100, blank=True, null=True)
    violationCode = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=225, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    evidencePic = models.FileField(blank=True, null=True)
    officerBatch = models.CharField(max_length=225, blank=True, null=True)
    signature = models.FileField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(default=get_deadline)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):

        return self.cellNumber


class Payment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    paymentBy = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    tx = models.CharField(max_length=250)


class Officer (models.Model):
    batchNumber = models.CharField(max_length=225)
    assignedDevice = models.CharField(max_length=225)
    dateCreated = models.DateTimeField('data created')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OfficerTickets (models.Model):
    ticket = models.IntegerField()

    def __str__(self):
        return self.ticket


class Address (models.Model):
    town = models.CharField(max_length=225)
    street = models.CharField(max_length=225)
    erf = models.CharField(max_length=225)

    def __str__(self):
        return self.town


class Restrictions (models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    dateCreated = models.DateTimeField('date Created')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LicCode (models.Model):
    code = models.CharField(max_length=225)
    description = models.TextField()
    dateCreated = models.DateTimeField('date Created')
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):

        return self.code
