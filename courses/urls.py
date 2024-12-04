from django.urls import path
from .views import (
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    LessonListView, LessonDetailView, LessonCreateView, LessonUpdateView, LessonDeleteView,
    LessonCompleteView, LessonUncompleteView,
    enroll_in_course, unenroll_from_course
)

urlpatterns = [
    # Курсы
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:id>/enroll/', enroll_in_course, name='enroll_in_course'),
    path('<int:pk>/unenroll/', unenroll_from_course, name='unenroll_from_course'),


    # Уроки
    path('<int:course_id>/lessons/', LessonListView.as_view(), name='lesson_list'),
    path('<int:course_id>/lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('<int:course_id>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('<int:course_id>/lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson_update'),
    path('<int:course_id>/lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('<int:course_id>/lessons/<int:pk>/complete/', LessonCompleteView.as_view(), name='lesson_complete'),
    path('<int:course_id>/lessons/<int:pk>/uncomplete/', LessonUncompleteView.as_view(), name='lesson_uncomplete'),

]
