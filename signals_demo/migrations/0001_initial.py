from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                            serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SignalLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                            serialize=False, verbose_name='ID')),
                ('thread_id', models.CharField(blank=True, max_length=100, null=True)),
                ('triggered_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
