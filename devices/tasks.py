from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .mailer import Mailer

# @shared_task
# def add(x, y):
#     return x + y


@shared_task
def mul(x, y):
    return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)

@shared_task()
def send_email(start, end, tool, recievers):
    mail = Mailer()
    print(recievers)
    # mail.send_messages(subject='TEST TEST TEST',
    #             template='emials/temp.html',
    #             context={'fname': 'x'},
    #             to_emails=['mehdikamaniii@gmail.com',])