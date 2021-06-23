from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader import fields

# Create your models here.
from django.urls import reverse_lazy


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    content = fields.RichTextUploadingField(verbose_name='Контент')
    video = models.URLField(blank=True, verbose_name='Видео')

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('lesson_num', kwargs={'lesson_id': self.pk})


class Question(models.Model):

    class Type(models.TextChoices):
        single = 'single_choice', 'Один ответ'
        multiple = 'multiple_choice', 'Несколько ответов'
        text = 'text_answer', 'Ответ в виде текста'

    text = models.TextField(verbose_name='Текст вопроса')
    type = models.CharField(max_length=40, choices=Type.choices, verbose_name='Тип')
    lesson = models.ForeignKey('Lesson', null=True, on_delete=models.PROTECT,
                               verbose_name='Занятие')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст')
    correct = models.BooleanField(verbose_name='Верно')
    question = models.ForeignKey('Question', null=True, on_delete=models.CASCADE,
                                 verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    answers = models.ManyToManyField('Question', through='Progress')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.user.username


class Progress(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    right = models.BooleanField()

    def __str__(self):
        return str(self.student) + ' - ' + str(self.question)
