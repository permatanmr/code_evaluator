# Generated by Django 3.2 on 2025-03-25 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluator', '0004_alter_question_programming_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='programming_language',
            field=models.CharField(choices=[('python', 'python'), ('javascript', 'javascript'), ('dart', 'dart')], max_length=50),
        ),
    ]
