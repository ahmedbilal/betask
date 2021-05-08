# Generated by Django 3.2.2 on 2021-05-08 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_auto_20210508_0530"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="articles.tag",
            ),
        ),
    ]
