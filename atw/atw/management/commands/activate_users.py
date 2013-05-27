"""
"""

from django.core.management.base import BaseCommand, CommandError
from utopia.models import UserProfile
from django.contrib import auth
from django.template.loader import render_to_string
from django.conf import settings

class Command(BaseCommand):
    help = 'Send emails to inactive users'

    def handle(self, *args, **options):
        profiles = UserProfile.objects.filter(user__is_active=False)
        for profile in profiles:
            user = profile.user
            w_email = render_to_string('email_reg1.html', {'user':user})
            try:
                user.email_user('After The Walls Registration', w_email)
                self.stdout.write('Email sent to %s <%s>' % (user.get_full_name(), user.email))
            except Exception:
                pass
            