from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Student)
admin.site.register(Answer)


class AnswerInline(admin.StackedInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]

