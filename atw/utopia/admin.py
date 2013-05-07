from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from utopia.models import *

class MediaInline(admin.TabularInline):
    model = Media
    extra = 1
    
class EpisodeAdmin(admin.ModelAdmin):
    inlines = [MediaInline]

admin.site.register(Episode, EpisodeAdmin)
admin.site.register(HomeImage)
admin.site.register(Media)