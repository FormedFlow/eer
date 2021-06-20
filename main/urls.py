from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutView.as_view(), name='about'),
    path('lessons/', LessonsList.as_view(), name='lessons'),
    path('lessons/<int:lesson_id>', lesson_detail, name='lesson_num'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile_view, name='profile')
]
