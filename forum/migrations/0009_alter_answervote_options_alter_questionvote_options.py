# Generated by Django 5.1.6 on 2025-03-07 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_answervote_questionvote'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answervote',
            options={'verbose_name': 'AnswerVote', 'verbose_name_plural': 'AnswerVotes'},
        ),
        migrations.AlterModelOptions(
            name='questionvote',
            options={'verbose_name': 'QuestionVote', 'verbose_name_plural': 'QuestionVotes'},
        ),
    ]
