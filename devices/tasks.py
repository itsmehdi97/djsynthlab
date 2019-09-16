from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .mailer import Mailer
from jalali_date import datetime2jalali, date2jalali
from datetime import datetime, timedelta

@shared_task()
def send_email(start, end, tool, receivers):
    start = datetime2jalali(prepare_datetime(start)).strftime('%y/%m/%d _ %H:%M:%S')
    end = datetime2jalali(prepare_datetime(end)).strftime('%y/%m/%d _ %H:%M:%S')
    mail = Mailer()
    mail.send_messages(subject='device schedule reminder',
                template='users/email_reminder.html',
                context={
                    'start': start,
                    'end': end,
                    'tool': tool,
                    },
                to_emails=receivers)


def prepare_datetime(dt):
    sdt = dt.split('+')[0].split('T')
    sd = sdt[0].split('-')
    st = sdt[1].split(':')
    return datetime(int(sd[0]), int(sd[1]), int(sd[2]), int(st[0]), int(st[1]), int(st[2])) + timedelta(hours=4, minutes=30)