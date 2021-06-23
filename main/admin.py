from django.contrib import admin

# Register your models here.

from .models import *


class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'right')
    search_fields = ('student__user__username', 'question__text')


admin.site.register(Progress, ProgressAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description', 'content')


admin.site.register(Lesson, LessonAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct', 'question')
    search_fields = ('text', 'question__text')


admin.site.register(Answer, AnswerAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('id', 'user__username')
    ordering = ['user']


admin.site.register(Student, StudentAdmin)


class AnswerInline(admin.StackedInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]

    list_display = ('text', 'type', 'lesson')
    search_fields = ('text', 'lesson__title', 'type')
    # ordering = ['text', 'type']

