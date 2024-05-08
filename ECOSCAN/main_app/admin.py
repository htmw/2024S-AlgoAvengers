from django.contrib import admin
from .models import Soils, Plants, Areas, SoilDetails

# Register your models here.

admin.site.register(Soils)
admin.site.register(Plants)
admin.site.register(Areas)
admin.site.register(SoilDetails)