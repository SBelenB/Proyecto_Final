# Generated by Django 4.2.7 on 2023-12-21 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0003_comentario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='texto',
            new_name='titulo',
        ),
    ]
