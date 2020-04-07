from django.core.management import call_command
import os


def my_scheduled_job():  # launch updatedb command / CRON TASK
    call_command('updatedb')
