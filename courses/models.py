from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_taught'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses_enrolled',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_lessons(self):
        """Возвращает общее количество уроков в курсе."""
        return self.lessons.count()

    def calculate_progress(self, student):
        """Возвращает процент завершения курса для конкретного студента."""
        total_lessons = self.total_lessons()
        if total_lessons == 0:
            return 0
        completed_lessons = Progress.objects.filter(student=student, course=self).first()
        if not completed_lessons:
            return 0
        return round((completed_lessons.completed_lessons.count() / total_lessons) * 100, 2)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  # Уроки сортируются по порядковому номеру

    def __str__(self):
        return f"{self.order}. {self.title}"

#custom user можно в парамент студента
class Progress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    def is_course_completed(self):
        """Проверяет, завершил ли студент курс."""
        return self.completed_lessons.count() == self.course.total_lessons()
