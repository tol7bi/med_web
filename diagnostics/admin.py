from django.contrib import admin

from diagnostics.models import ChemicalAnalyzes, GeneralAnalyzes

# Register your models here.

@admin.register(GeneralAnalyzes)
class GeneralAnalyzesAdmin(admin.ModelAdmin):
    search_fields = ('Название поля',)
    ordering = ('Название поля',)

@admin.register(ChemicalAnalyzes)
class ChemicalAnalyzesAdmin(admin.ModelAdmin):
    search_fields = ('Название поля',)
    ordering = ('Название поля',)