from django import forms
from .models import Course, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # fields = ('title', 'description', 'teacher', 'students')
        fields = ('title', 'description')

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('course', 'title', 'content', 'order')
