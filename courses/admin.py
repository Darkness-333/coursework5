from django.contrib import admin
from .models import Course, Lesson, Progress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('students',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    ordering = ('course', 'order')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__title')


# admin.site.register(Course)
# admin.site.register(Lesson)
# admin.site.register(Progress)
