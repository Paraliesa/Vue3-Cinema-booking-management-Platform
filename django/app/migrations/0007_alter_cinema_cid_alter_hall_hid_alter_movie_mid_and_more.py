# Generated by Django 5.1.4 on 2024-12-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_place_pid_alter_type_tid_alter_user_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='cid',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='电影院编号'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='hid',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='影厅编号'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='mid',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='电影编号'),
        ),
        migrations.AlterField(
            model_name='seatmodel',
            name='sid',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='布局模板编号'),
        ),
    ]
