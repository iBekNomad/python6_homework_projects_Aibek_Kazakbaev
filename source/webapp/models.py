from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator


class Type(models.Model):
    type = models.CharField(max_length=40, null=False, blank=False, verbose_name='Type')

    def __str__(self):
        return f'{self.type}'


class Status(models.Model):
    status = models.CharField(max_length=40, null=False, blank=False, verbose_name='Status')

    def __str__(self):
        return f'{self.status}'


class Issue(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Title')
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Description',
                                   validators=[MinLengthValidator(25)])
    status = models.ForeignKey('webapp.Status', related_name='issues_statuses', on_delete=models.PROTECT,
                               verbose_name='Status')
    type = models.ManyToManyField('webapp.Type', related_name='issues_types', blank=True, verbose_name='Type')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')
    project = models.ForeignKey('webapp.Project', default=1, related_name='issues', on_delete=models.PROTECT,
                                verbose_name='project')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'


class Project(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='Name')
    description = models.TextField(max_length=2000, null=False, blank=False, verbose_name='Project Description')
    start_date = models.DateField(null=False, blank=False, verbose_name='Start date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End date')
    user = models.ManyToManyField(get_user_model(), related_name='projects', verbose_name='Ползователь')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

