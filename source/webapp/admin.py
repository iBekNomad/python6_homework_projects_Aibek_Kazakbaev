from django.contrib import admin
from webapp.models import Issue, Type, Status, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')
    search_fields = ('title',)


class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


class IssueTypesAdmin(admin.ModelAdmin):
    list_display = ('type',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status, IssueStatusAdmin)
admin.site.register(Type, IssueTypesAdmin)
admin.site.register(Project, ProjectAdmin)
