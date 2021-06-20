from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader import fields

# Create your models here.
from django.urls import reverse_lazy


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    content = fields.RichTextUploadingField()
    video = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('lesson_num', kwargs={'lesson_id': self.pk})


class Question(models.Model):

    class Type(models.TextChoices):
        single = 'single_choice', 'Single choice'
        multiple = 'multiple_choice', 'Multiple choice'
        text = 'text_answer', 'Text answer'

    text = models.TextField()
    type = models.CharField(max_length=40, choices=Type.choices)
    lesson = models.ForeignKey('Lesson', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField()
    question = models.ForeignKey('Question', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    answers = models.ManyToManyField('Question', through='Progress')

    def __str__(self):
        return self.user.username


class Progress(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    right = models.BooleanField()

    def __str__(self):
        return str(self.student) + ' - ' + str(self.question)
