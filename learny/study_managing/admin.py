from django.contrib import admin
from .models import Teacher, Student, Enrollment, Homework, SubmittedHomework, Course, Attendance
# Register your models here.

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status')
    search_fields = ('student__name', 'course__title')
    list_filter = ('status', 'course')
    ordering = ('-enrollment_date',)


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'dob', 'phone_number')
    search_fields = ('name', 'email')
    ordering = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'specialization', 'phone_number')
    search_fields = ('name', 'email', 'specialization')
    ordering = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'teacher', 'start_date', 'max_students')
    search_fields = ('title', 'description', 'teacher__name')
    list_filter = ('teacher', 'start_date')
    ordering = ('-start_date',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'isPresent')
    search_fields = ('enrollment__student__name', 'enrollment__course__title')
    list_filter = ('date', 'isPresent', 'enrollment__course')
    ordering = ('-date',)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'submission_date')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'submission_date')
    ordering = ('-submission_date',)

@admin.register(SubmittedHomework)
class SubmittedHomeworkAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submitted_at', 'grade')
    search_fields = ('homework__title', 'student__name')
    list_filter = ('grade', 'submitted_at', 'homework__course')
    ordering = ('-submitted_at',)