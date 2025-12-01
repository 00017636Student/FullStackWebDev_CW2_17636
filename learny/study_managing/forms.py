from django.forms import ModelForm
from django import forms
from .models import Teacher, Student, Course, Homework, SubmittedHomework, Attendance, Enrollment
from django.core.exceptions import ValidationError

class BaseStyledModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

class TeacherForm(BaseStyledModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.startswith("998") or len(phone) != 12:
            raise ValidationError("You should write your number as: 998xxxxxxxxx")
        return phone

class StudentForm(BaseStyledModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.startswith("998") or len(phone) != 12:
            raise ValidationError("You should write your number as: 998xxxxxxxxx")
        return phone

class CourseForm(BaseStyledModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date'
         })
        }

class HomeworkForm(BaseStyledModelForm):
    class Meta:
        model = Homework
        fields = '__all__'
        widgets = {
            'submission_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Select date and time'
         })
        }

class SubmittedHomeworkStudentForm(BaseStyledModelForm): #This form will be used by student to send his hw
    class Meta:
        model = SubmittedHomework
        fields = ['submitted_file']

class SubmittedHomeworkTeacherForm(BaseStyledModelForm): #This form will be used by teacher to put grade and feedback
    class Meta:
        model = SubmittedHomework
        fields = ['grade', 'feedback']

class AttendanceForm(BaseStyledModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        labels = {
            'enrollment': 'Student',
            'date': 'Attendance Date',
            'isPresent': 'Present?',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'isPresent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *args, teacher_profile=None, **kwargs):
        super().__init__(*args, **kwargs)

        if teacher_profile:
            teacher_courses = teacher_profile.course_set.all()
            
            self.fields['enrollment'].queryset = Enrollment.objects.filter(
                course__in=teacher_courses
            ).select_related('student', 'course').order_by('course__title', 'student__name')
            

class EnrollmentForm(BaseStyledModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']



