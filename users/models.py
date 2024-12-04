from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def taught_courses(self):
        """Возвращает курсы, которые пользователь-преподаватель ведет."""
        if self.role == 'teacher':
            return self.courses_taught.all()
        return None

    def enrolled_courses(self):
        """Возвращает курсы, на которые записан студент."""
        if self.role == 'student':
            return self.courses_enrolled.all()
        return None
