from django.contrib import admin
from example2.forms import CForm
from example2.models import A, B, C
from django.contrib import admin
from nested_inlines.admin import (NestedModelAdmin, NestedTabularInline,
                                  NestedStackedInline)


class CInline(NestedTabularInline):
    model = C
    extra = 1
    max_num = 1
    form = CForm


class BInline(NestedStackedInline):
    model = B
    extra = 1
    max_num = 1
    inlines = [CInline, ]


class AAdmin(NestedModelAdmin):
    inlines = [BInline, ]

admin.site.register(A, AAdmin)
