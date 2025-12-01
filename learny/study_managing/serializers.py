from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='enrollment.student.name', read_only=True)
    course_title = serializers.CharField(source='enrollment.course.title', read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = Homework
        fields = '__all__'

class SubmittedHomeworkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    homework_title = serializers.CharField(source='homework.title', read_only=True)
    class Meta:
        model = SubmittedHomework
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = Enrollment
        fields = '__all__'