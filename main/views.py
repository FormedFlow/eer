from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *
from .models import *

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .utils import DataMixin, menu


class HomePageView(DataMixin, TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        added_context = self.get_user_context(title='Уроки по Django - Главная')
        return {**context, **added_context}


class ContactsView(DataMixin, TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        added_context = self.get_user_context()
        return {**context, **added_context}


class AboutView(DataMixin, TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        added_context = self.get_user_context()
        return {**context, **added_context}


class LessonsList(DataMixin, ListView):
    model = Lesson
    template_name = 'main/lessons.html'
    context_object_name = 'lesson_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        added_context = self.get_user_context(title='Уроки')
        return {**context, **added_context}


# class LessonDetail(DataMixin, DetailView):
#     model = Lesson
#     pk_url_kwarg = 'lesson_id'
#     context_object_name = 'lesson'
#     template_name = 'main/lesson_detailed.html'
#     time = datetime.now()
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(self.kwargs['lesson_id'])
#         added_context = self.get_user_context()
#         return {**context, **added_context}

def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    questions = Question.objects.filter(lesson=lesson)
    questions_count = Question.objects.count()
    prefix_gen = (str(i) for i in range(questions_count))
    quiz_forms = []

    if request.method == 'POST':
        for question in questions:
            print(question)
            if question.type == 'text_answer':
                quiz_forms.append(TextAnswerForm(request.POST,
                                                 label=question.text, prefix=next(prefix_gen)))
                form_type = 'text_answer'
            if question.type == 'single_choice':
                quiz_forms.append(SingleChoiceForm(request.POST,
                                                   question=question, prefix=next(prefix_gen)))
                form_type = 'single_choice'
            if question.type == 'multiple_choice':
                quiz_forms.append(MultipleChoicesForm(request.POST,
                                                      question=question, prefix=next(prefix_gen)))
                form_type = 'multiple_choice'
            quiz_forms[-1].is_valid()
            print(quiz_forms[-1])
            created = False
            right_answers = Answer.objects.filter(question=question).filter(correct=True)
            if form_type == 'text_answer' or form_type == 'single_choice':
                for answer in right_answers:
                    print(str(answer.text))
                    print(str(quiz_forms[-1].cleaned_data['answer']))
                    print(str(answer.text) == str(quiz_forms[-1].cleaned_data['answer']))
                    if str(answer.text) == str(quiz_forms[-1].cleaned_data['answer']):
                        Progress.objects.create(student=Student.objects.get(user=request.user),
                                                question=question,
                                                right=True)
                        created = True
                if not created:
                    Progress.objects.create(student=Student.objects.get(user=request.user),
                                            question=question,
                                            right=False)

            if form_type == 'multiple_choice':
                print(f"{list(quiz_forms[-1].cleaned_data.get('answer'))}, что имеем в форме")
                print(f"{list(right_answers)}, а это правильные ответы")
                print(list(quiz_forms[-1].cleaned_data.get('answer')) == list(right_answers))
                if list(quiz_forms[-1].cleaned_data.get('answer')) == list(right_answers):
                    Progress.objects.create(student=Student.objects.get(user=request.user),
                                            question=question,
                                            right=True)
                    created = True
                if not created:
                    Progress.objects.create(student=Student.objects.get(user=request.user),
                                            question=question,
                                            right=False)

        context = {'lesson': lesson, 'forms': quiz_forms, 'menu': menu}
        return render(request, 'main/lesson_detailed.html', context=context)

    else:
        for question in questions:
            answers = Answer.objects.filter(question=question)
            if question.type == 'text_answer':
                quiz_forms.append(TextAnswerForm(label=question.text, prefix=next(prefix_gen)))
            if question.type == 'single_choice':
                quiz_forms.append(SingleChoiceForm(question=question, prefix=next(prefix_gen)))
            if question.type == 'multiple_choice':
                quiz_forms.append(MultipleChoicesForm(question=question, prefix=next(prefix_gen)))

    context = {'lesson': lesson, 'forms': quiz_forms, 'menu': menu}
    return render(request, 'main/lesson_detailed.html', context=context)


class UserRegistration(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'main/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        added_context = self.get_user_context(title='Регистрация')
        return {**context, **added_context}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        added_context = self.get_user_context(title='Вход')
        return {**context, **added_context}


def logout_user(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    student = Student.objects.get(user=request.user)
    print(student)
    lessons = Lesson.objects.all()
    progress = []
    grades = []
    have_passed = []
    for lesson in lessons:
        questions = Question.objects.filter(lesson=lesson)
        print(questions)
        progress_entries = Progress.objects.filter(student=student).filter(question__in=questions)
        if not progress_entries:
            progress.append(0)
            grades.append(0)
            have_passed.append(False)
        else:
            print(progress_entries)
            progress_entries_right = progress_entries.filter(right=True)
            result = int(progress_entries_right.count()/questions.count() * 100)
            print(result)
            progress.append(result)
            if result <= 40:
                grades.append(2)
            elif result <= 55:
                grades.append(3)
            elif result <= 85:
                grades.append(4)
            elif result <= 100:
                grades.append(5)
            have_passed.append(True)
    lessons_progress = list(zip(lessons, progress, grades, have_passed))
    for item in lessons_progress:
        print(item[0].get_absolute_url())
    context = {'lessons': lessons_progress, 'menu': menu}
    return render(request, 'main/profile.html', context=context)




