# Generated by Django 2.2.13 on 2020-08-09 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=40, verbose_name='Type')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Description')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues_statuses', to='webapp.Status', verbose_name='Status')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues_types', to='webapp.Type', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issues',
            },
        ),
    ]
