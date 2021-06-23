from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import CheckboxSelectMultiple, TextInput, RadioSelect

from .models import Question, Answer


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class MultipleChoicesForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(queryset=Answer.objects.none(),
                                            to_field_name="text",
                                            widget=CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(MultipleChoicesForm, self).__init__(*args, **kwargs)
        outer_question = kwargs.pop('question')
        self.fields['answer'].label = outer_question.text
        # self.fields['answer'].queryset = Answer.objects.filter(question=outer_question)


class SingleChoiceForm(forms.Form):
    answer = forms.ModelChoiceField(queryset=Answer.objects.none(),
                                    to_field_name="text",
                                    widget=RadioSelect(),
                                    empty_label=None)

    def __init__(self, *args, **kwargs):
        outer_question = kwargs.pop('question')
        super(SingleChoiceForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = outer_question.text
        self.fields['answer'].queryset = Answer.objects.filter(question=outer_question)
        # label = kwargs.pop('label')
        # queryset = kwargs.pop('queryset')
        # super(SingleChoiceForm, self).__init__(*args, **kwargs)
        # self.fields['answer_single'].label = label
        # self.fields['answer_single'].queryset = queryset


class TextAnswerForm(forms.Form):
    answer= forms.CharField(max_length=255, widget=TextInput(attrs={
        'class': 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label')
        super(TextAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = label
