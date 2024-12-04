from .views import account, auth_selection
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from courses.views import CourseListView

urlpatterns = [
    path('account/', account, name='account'),
    path('auth/', auth_selection, name='auth'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', CourseListView.as_view(), name='course_list'),
]
