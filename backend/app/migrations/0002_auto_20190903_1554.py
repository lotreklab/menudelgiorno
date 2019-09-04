# Generated by Django 2.2.4 on 2019-09-03 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='consumeDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='sendDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='ContentMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Menu')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='courses',
            field=models.ManyToManyField(through='app.ContentMenu', to='app.Course'),
        ),
    ]