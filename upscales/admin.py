from django.contrib import admin
from upscales.models import Upscale

# Register your models here.


class UpscaleAdmin(admin.ModelAdmin):
    fields = ('gt', 'name', 'upscale_model')


admin.site.register(Upscale, UpscaleAdmin)
