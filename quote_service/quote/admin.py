from django.contrib import admin
from .models import Source, Quote, Opinion, WorkType


class QuoteInLine(admin.StackedInline):
    model = Quote


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    inlines = (
        QuoteInLine,
    )
    list_display = ('title',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'source', 'text', 'views', 'weight'
    )
    search_fields = ('author', 'source', 'text')
    list_editable = ('weight',)
    list_filter = ('views', 'weight')
    empty_value_display = 'Не задано'


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quote', 'value', 'created_at')
    list_display_links = ('quote',)


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    pass