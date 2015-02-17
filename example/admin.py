from django.contrib import admin
from example.forms import StandardModelForm
from example.models import *


class StandardModelAdmin(admin.ModelAdmin):
    model = StandardModel
    form = StandardModelForm


admin.site.register(StandardModel, StandardModelAdmin)
