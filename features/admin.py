from django.contrib import admin
from .models import Feature

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'feature_type', 'size')
    search_fields = ('name', 'feature_type')
