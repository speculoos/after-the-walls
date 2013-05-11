"""
utopia.translation
"""

from modeltranslation.translator import translator, TranslationOptions
from utopia.models import *

class EpisodeTrOptions(TranslationOptions):
    fields = ('title','body',)
    
    

translator.register(Episode, EpisodeTrOptions)