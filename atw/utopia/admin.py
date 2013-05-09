from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from utopia.models import *


admin.site.register(Episode)
admin.site.register(HomeImage)
admin.site.register(Media)
admin.site.register(Message)
admin.site.register(UserProfile)