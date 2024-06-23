from django.contrib import admin
from .models import Upper, Lower, MatchingCombination

# Register your models here.
admin.site.register(Upper)
admin.site.register(Lower)
admin.site.register(MatchingCombination)