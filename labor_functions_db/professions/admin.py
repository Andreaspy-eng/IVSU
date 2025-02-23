from django.contrib import admin
from .models import *

admin.site.register(Profession)
admin.site.register(GeneralizedLaborFunction)
admin.site.register(LaborFunction)
admin.site.register(LaborAction)
admin.site.register(RequiredSkill)
admin.site.register(RequiredKnowledge)
admin.site.register(OKSO)