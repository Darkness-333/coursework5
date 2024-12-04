from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')  # Возвращаем шаблон для главной страницы


@login_required
def account(request):
    return render(request, 'users/account.html')


def auth_selection(request):
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()

    # Проверка, какая форма была выбрана
    if 'show_register' in request.POST:
        request.session['form_type'] = 'register'
    elif 'show_login' in request.POST:
        request.session['form_type'] = 'login'

    form_type = request.session.get('form_type', 'login')  # По умолчанию показываем форму входа

    # Обработка входа
    if form_type == 'login' and request.method == 'POST' and 'login' in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('index')  # Перенаправляем на главную страницу

    # Обработка регистрации
    elif form_type == 'register' and request.method == 'POST' and 'register' in request.POST:
        register_form = CustomUserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('index')  # Перенаправляем на главную страницу

    # Отображаем страницу с формами
    return render(request, 'users/auth_selection.html', {
        'login_form': login_form,
        'register_form': register_form,
        'form_type': form_type,
    })

from courses.models import Course, Progress

@login_required
def profile(request):
    user = request.user
    if user.role == 'student':
        enrolled_courses = user.enrolled_courses()
        progress_data = []
        for course in enrolled_courses:
            progress = Progress.objects.filter(student=user, course=course).first()
            progress_data.append({
                'course': course,
                'completed_lessons': progress.completed_lessons.count() if progress else 0,
                'total_lessons': course.lessons.count(),
                'course_id': course.id  # Добавляем ID курса в данные
            })
        return render(request, 'users/profile_student.html', {'courses': progress_data})

    elif user.role == 'teacher':
        taught_courses = user.taught_courses()
        return render(request, 'users/profile_teacher.html', {'courses': taught_courses})
