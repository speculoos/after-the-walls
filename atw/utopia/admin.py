from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from modeltranslation.admin import TranslationAdmin

from utopia.models import *

class TabbedTr:
    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name','location','languages','skills','interests','is_active')
        
class EpisodeAdmin(TabbedTr, TranslationAdmin):
    list_display = ('title', 'pub_date')
        
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(HomeImage)
admin.site.register(Media)
admin.site.register(Message)
admin.site.register(UserProfile, UserProfileAdmin)