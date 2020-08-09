from django.contrib import admin
from webapp.models import Issue, Type, Status


class IssueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')
    search_fields = ('title',)


class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


class IssueTypesAdmin(admin.ModelAdmin):
    list_display = ('type',)


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status, IssueStatusAdmin)
admin.site.register(Type, IssueTypesAdmin)
