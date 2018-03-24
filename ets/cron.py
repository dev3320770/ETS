from django.core.management.base import BaseCommand, CommandError
from ets.models import User
from datetime import timedelta
import datetime
import kronos


@kronos.register('* 1 * * *')
class Command(BaseCommand):

    args = ''

    def my_scheduled_job(self, *args, **options):

        today = datetime.date.today() 
        User.objects.filter(username='admin').update(first_name='festus')