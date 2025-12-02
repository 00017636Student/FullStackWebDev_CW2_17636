from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher (models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_profile')

    def __str__(self):
        return f"{self.name} ({self.specialization})"
    
class Student (models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    def __str__(self):
        return f"{self.name} ({self.dob})"
    
class Course (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    max_students = models.IntegerField(default=10)
    def __str__(self):
        return f"{self.title}"
    
class Enrollment (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add= True)
    status = models.CharField(max_length=20, default= "enrolled")
    class Meta:
        unique_together = ('student', 'course') #Ensures that student is not enrolled multiple times to the same course
    def __str__(self):
        return f"{self.student.name} → {self.course.title}"

class Attendance (models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    isPresent = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.enrollment.student.name} ({self.date:%Y-%m-%d})"
    
class Homework (models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    title = models.CharField(max_length= 100)
    description = models.TextField()
    submission_date = models.DateTimeField() #deadline
    def __str__(self):
        return f"{self.course.title} ({self.title})"
    
class SubmittedHomework(models.Model):
    grade_choices = [
        ('pass', 'Pass'), # pass is stored in database, Pass is shown
        ('fail','Fail'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_text = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=10, choices = grade_choices, blank=True, null=True)
    def __str__(self):
        return f"{self.homework.title} ({self.submitted_at})"
    



