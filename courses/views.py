from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, Lesson
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def enroll_in_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.user.role == 'student' and request.user not in course.students.all():
        course.students.add(request.user)
    return redirect('course_detail', pk=course.id)


@login_required
def unenroll_from_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        if request.user.role == 'student' and request.user in course.students.all():
            course.students.remove(request.user)
    return redirect('course_list')



from django.db.models import Q


# Список курсов
# class CourseListView(LoginRequiredMixin, ListView):
#     model = Course
#     template_name = 'courses/course_list.html'
#     context_object_name = 'courses'
#
#     def get_queryset(self):
#         queryset = Course.objects.all()
#         search_query = self.request.GET.get('search', '')
#         if search_query:
#             queryset = queryset.filter(Q(title__icontains=search_query))
#         return queryset

# class CourseListView(LoginRequiredMixin, ListView):
#     model = Course
#     template_name = 'courses/course_list.html'
#     context_object_name = 'courses'
#
#     def get_queryset(self):
#         queryset = Course.objects.all()
#         search_query = self.request.GET.get('search', '')
#
#         if search_query:
#             # Фильтр по названию курса
#             queryset = queryset.filter(Q(title__icontains=search_query))
#
#         if self.request.user.role == 'teacher':
#             # Для учителя отображаются только его курсы
#             queryset = queryset.filter(teacher=self.request.user)
#         else:
#             # Для студента отображаются курсы, на которые он записан
#             queryset = queryset.filter(students=self.request.user)
#
#         return queryset.order_by('-created_at')  # Сортировка по дате добавления

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = Course.objects.all()
        search_query = self.request.GET.get('search', '')
        filter_option = self.request.GET.get('filter', 'all')

        # Фильтр по названию курса
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        # Фильтрация по роли или участию
        if filter_option == 'teacher':
            queryset = queryset.filter(teacher=self.request.user)  # Курсы, которые ведет учитель
        elif filter_option == 'student':
            queryset = queryset.filter(students=self.request.user)  # Курсы, на которые записан студент
        elif filter_option == 'unrelated':
            queryset = queryset.exclude(Q(teacher=self.request.user) | Q(students=self.request.user))  # Курсы, к которым пользователь не относится

        return queryset.order_by('-created_at')  # Сортировка по дате добавления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')  # Передача текущего фильтра в контекст
        return context


# Детали курса
# class CourseDetailView(LoginRequiredMixin, DetailView):
#     model = Course
#     template_name = 'courses/course_detail.html'
#     context_object_name = 'course'

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        user_progress = Progress.objects.filter(student=self.request.user, course=course).first()
        completed_lessons = user_progress.completed_lessons.all() if user_progress else []
        context['completed_lessons'] = completed_lessons
        return context

# Создание курса
class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.role == 'teacher'

# Редактирование курса
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.teacher

# Удаление курса
class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.teacher


# Список уроков
class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'courses/lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return course.lessons.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']  # Передаем course_id в контекст
        return context

# Детали урока
# class LessonDetailView(LoginRequiredMixin, DetailView):
#     model = Lesson
#     template_name = 'courses/lesson_detail.html'
#     context_object_name = 'lesson'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Добавляем course_id в контекст
#         # context['course_id'] = self.kwargs['course_id']
#         context['course_id'] = self.object.course.id
#
#         return context

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['course_id'] = course_id

        # Добавляем информацию о завершенных уроках для текущего студента
        if self.request.user.role == 'student':
            progress = Progress.objects.filter(student=self.request.user, course_id=course_id).first()
            context['completed_lessons'] = progress.completed_lessons.all() if progress else []
        return context


# Создание урока
# class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Lesson
#     fields = ['title', 'content', 'order']
#     template_name = 'courses/lesson_form.html'
#
#     def form_valid(self, form):
#         course = get_object_or_404(Course, pk=self.kwargs['course_id'])
#         form.instance.course = course
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('lesson_list', kwargs={'course_id': self.kwargs['course_id']})
#
#     def test_func(self):
#         course = get_object_or_404(Course, pk=self.kwargs['course_id'])
#         return self.request.user == course.teacher
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['course_id'] = self.kwargs['course_id']
#         return context

class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    fields = ['title', 'content', 'order']  # Поля формы
    template_name = 'courses/lesson_form.html'

    def form_valid(self, form):
        # Привязываем урок к курсу
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        # Возврат к странице деталей курса
        return reverse_lazy('course_detail', kwargs={'pk': self.kwargs['course_id']})

    def test_func(self):
        # Проверяем, что пользователь — преподаватель курса
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return self.request.user == course.teacher

    def get_context_data(self, **kwargs):
        # Передаем ID курса в контекст для использования в шаблоне
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context

# Редактирование урока
class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    fields = ['title', 'content', 'order']
    template_name = 'courses/lesson_form.html'

    # def get_success_url(self):
    #     return reverse_lazy('lesson_list', kwargs={'course_id': self.object.course.id})

    def get_success_url(self):
        # Возврат к странице деталей курса
        return reverse_lazy('course_detail', kwargs={'pk': self.kwargs['course_id']})

    def test_func(self):
        lesson = self.get_object()
        return self.request.user == lesson.course.teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


# Удаление урока
class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = 'courses/lesson_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('lesson_list', kwargs={'course_id': self.object.course.id})

    def test_func(self):
        lesson = self.get_object()
        return self.request.user == lesson.course.teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Lesson, Progress, Course

class LessonCompleteView(View):
    def post(self, request, course_id, pk):
        # Получаем урок по id и курсу
        lesson = get_object_or_404(Lesson, pk=pk, course_id=course_id)
        student = request.user

        # Находим или создаем объект Progress для студента и курса
        progress, created = Progress.objects.get_or_create(student=student, course=lesson.course)

        # Добавляем урок в список завершенных
        progress.completed_lessons.add(lesson)
        progress.save()

        # Перенаправляем на страницу списка уроков
        return redirect('course_detail', pk=course_id)

class LessonUncompleteView(View):
    def post(self, request, course_id, pk):
        # Получаем урок по id и курсу
        lesson = get_object_or_404(Lesson, pk=pk, course_id=course_id)
        student = request.user

        # Проверяем, существует ли объект Progress для студента и курса
        progress = Progress.objects.filter(student=student, course=lesson.course).first()

        # Если Progress существует, удаляем урок из завершенных
        if progress:
            progress.completed_lessons.remove(lesson)
            progress.save()

        # Перенаправляем на страницу списка уроков
        return redirect('course_detail', pk=course_id)
