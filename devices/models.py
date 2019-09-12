from django.db import models
from django.utils import timezone

from jalali_date import datetime2jalali, date2jalali
from datetime import datetime 

from users.models import User


class Tool(models.Model):
    # type = models.ForeignKey(ToolType, on_delete=models.CASCADE, related_name='tools')
    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Attr(models.Model):
    key = models.CharField(max_length=32, unique=True)
    # data_type = models.CharField(max_length=16)

    def __str__(self):
        return self.key


class ToolAttr(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    attr = models.ForeignKey(Attr, on_delete=models.CASCADE)
    value = models.CharField(max_length=300)

    def __str__(self):
        return "{}.{} = {}".format(self.tool.name, self.attr.key, self.value)


class Reservation(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    users = models.ManyToManyField(User, db_table='devices_reservation_users', related_name='reservations', blank=True) 
    desc = models.TextField(null=True, blank=True)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='tool_reservations')
    
    @property
    def status(self):
        now = timezone.now()
        if self.start < now < self.end:
            return 'in progress'
        elif now < self.start:
            return 'queued'
        else:
            return 'expired'
        

    @property
    def start_datetime(self):
        return datetime2jalali(self.start).strftime('%y/%m/%d _ %H:%M:%S')

    @property
    def end_datetime(self):
        return datetime2jalali(self.end).strftime('%y/%m/%d _ %H:%M:%S')

    def __str__(self):
        return "{}".format(self.tool)

    @property
    def reserved_by(self):
        if not self.users:
            return '-'
        rv = ''
        for user in self.users.all():
            rv += str(user) + ", "
        return rv[:-2]


class ReservationAttr(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    attr = models.ForeignKey(Attr, on_delete=models.CASCADE)
    value = models.CharField(max_length=300)