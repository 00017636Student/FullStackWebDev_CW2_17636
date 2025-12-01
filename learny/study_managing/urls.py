from . import views
from .views import EnrollmentCreateView, EnrollmentDeleteView, HomeworkCreateView, HomeworkUpdateView, HomeworkDeleteView, AttendanceCreateView, AttendanceUpdateView
from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views_api import (
    StudentViewSet,
    TeacherViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    HomeworkViewSet,
    SubmittedHomeworkViewSet,
    AttendanceViewSet
)

#API router
router = DefaultRouter()
router.register("students", StudentViewSet)
router.register("teachers", TeacherViewSet)
router.register("courses", CourseViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("homeworks", HomeworkViewSet)
router.register("submitted-homeworks", SubmittedHomeworkViewSet)
router.register("attendances", AttendanceViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('teachers/', views.teachers_list, name='teachers'),
    path('students/', views.students_list, name='students'),
    path('courses/', views.courses_list, name='courses'),
    path('enrollments/', views.enrollments_list, name='enrollments'),
    path('attendances/', views.attendances_list, name='attendances'),
    path('homeworks/', views.homeworks_list, name='homeworks'),
    path('submitted-homeworks/', views.submitted_homeworks_list, name='submitted_homeworks'),

    path('homeworks/details/<int:pk>/', views.homework_details, name='homework_details'),
    path('submitted-homeworks/details/<int:pk>/', views.submittedHomework_details, name='submitted_homeworks_details'),

    path('teachers/create/', views.create_teacher, name='create_teacher'),
    path('students/create/', views.create_student, name='create_student'),
    path('courses/create/', views.create_course, name='create_course'),
    path('enrollments/create/', EnrollmentCreateView.as_view(), name='create_enrollment'),
    path('attendances/create/', AttendanceCreateView.as_view(), name='create_attendance'),
    path('homeworks/create/', HomeworkCreateView.as_view(), name='create_homework'),

    path('submitted-homeworks/submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('submitted-homeworks/grade/<int:submission_id>/', views.grade_homework, name='grade_homework'),

    path('teachers/update/<int:id>/', views.update_teacher, name='update_teacher'),
    path('students/update/<int:id>/', views.update_student, name='update_student'),
    path('courses/update/<int:id>/', views.update_course, name='update_course'),
    path('attendances/update/<int:pk>/', AttendanceUpdateView.as_view(), name='update_attendance'),
    path('homeworks/update/<int:pk>/', HomeworkUpdateView.as_view(), name='update_homework'),


    path('teachers/delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('enrollments/delete/<int:pk>/', EnrollmentDeleteView.as_view(), name='delete_enrollment'),
    path('homeworks/delete/<int:pk>/', HomeworkDeleteView.as_view(), name='delete_homework'),
    path('submitted-homeworks/delete/<submission_id>/', views.delete_submittedHomework, name='delete_submittedHomework'),

    path("api/", include(router.urls)),
]

handler403 = "scheduling.views.custom_permission_denied_view"


