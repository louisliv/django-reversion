# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 16:00
from __future__ import unicode_literals

from django.db import migrations, models, router


def set_version_db(apps, schema_editor):
    """
    Updates the db field in all Version models to point to the correct write
    db for the model.
    """
    Version = apps.get_model("reversion", "Version")
    content_types = Version.objects.values_list("content_type", flat=True).distinct()
    for content_type in content_types:
        model = content_type.model_class()
        db = router.db_for_write(model)
        Version.objects.filter(content_type=content_type).update(db=db)


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '0002_auto_20141216_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revision',
            name='manager_slug',
        ),
        migrations.RemoveField(
            model_name='version',
            name='object_id_int',
        ),
        migrations.AlterField(
            model_name='version',
            name='object_id',
            field=models.CharField(help_text='Primary key of the model under version control.', max_length=191),
        ),
        migrations.AlterField(
            model_name='revision',
            name='date_created',
            field=models.DateTimeField(db_index=True, help_text='The date and time this revision was created.', verbose_name='date created'),
        ),
        migrations.AddField(
            model_name='version',
            name='db',
            field=models.CharField(null=True, help_text='The database the model under version control is stored in.', max_length=191),
        ),
        migrations.RunPython(set_version_db),
        migrations.AlterField(
            model_name='version',
            name='db',
            field=models.CharField(help_text='The database the model under version control is stored in.', max_length=191),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('db', 'content_type', 'object_id', 'revision')]),
        ),
    ]
