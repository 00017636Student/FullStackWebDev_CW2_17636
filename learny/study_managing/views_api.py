from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Student, Teacher, Course, Enrollment, Homework, SubmittedHomework, Attendance
from .serializers import (StudentSerializer, TeacherSerializer, CourseSerializer, EnrollmentSerializer, HomeworkSerializer, SubmittedHomeworkSerializer, AttendanceSerializer) 
from django.utils import timezone

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        student = request.data.get("student")
        course = request.data.get("course")
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {"detail": "Student is already enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class SubmittedHomeworkViewSet(viewsets.ModelViewSet):
    queryset = SubmittedHomework.objects.all()
    serializer_class = SubmittedHomeworkSerializer

    def create(self, request, *args, **kwargs):
        homework_id = request.data.get("homework")
        homework = Homework.objects.get(id=homework_id)

        if homework.submission_date and timezone.now() > homework.submission_date:
            return Response(
                {"detail": "Deadline has passed — submission not allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

