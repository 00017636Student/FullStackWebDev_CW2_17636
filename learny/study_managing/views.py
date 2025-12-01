from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import TeacherForm, StudentForm, CourseForm, AttendanceForm, HomeworkForm, EnrollmentForm, SubmittedHomeworkStudentForm, SubmittedHomeworkTeacherForm 
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from datetime import UTC

# Create your views here.
def custom_permission_denied_view(request, exception=None): #Function for custom 403 page
    return render(request, "403.html", status=403)

@login_required
def home(request):
    user = request.user
    context = {}

    if user.is_superuser:
        context['students_count'] = Student.objects.count()
        context['teachers_count'] = Teacher.objects.count()
        context['courses_count'] = Course.objects.count()
        context['enrollments_count'] = Enrollment.objects.count()

    if hasattr(user, 'teacher_profile'):
        teacher_courses = Course.objects.filter(teacher=user.teacher_profile)
        enrolled_students_count = Enrollment.objects.filter(course__in=teacher_courses).values('student').distinct().count()
        homeworks_count = Homework.objects.filter(course__in=teacher_courses).count()
        submissions_to_grade = SubmittedHomework.objects.filter(homework__course__in=teacher_courses, grade__isnull=True)
        context.update({
            'teacher_courses': teacher_courses,
            'enrolled_students_count': enrolled_students_count,
            'homeworks_count': homeworks_count,
            'submissions_to_grade': submissions_to_grade
        })

    if hasattr(user, 'student_profile'):
        student = user.student_profile
        student_courses = Course.objects.filter(enrollments__student=student)
        context['student_courses'] = student_courses

    return render(request, 'home.html', context)

#Get all
@login_required
@permission_required("study_managing.view_teacher", raise_exception=True)
def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'Teachers/teachers.html', {'teachers': teachers})

@login_required
@permission_required("study_managing.view_student", raise_exception=True)
def students_list(request):
    students = Student.objects.all()
    return render(request, 'Students/students.html', {'students': students})

@login_required
@permission_required("study_managing.view_course", raise_exception=True)
def courses_list(request):
    user= request.user
    courses = Course.objects.none()
    if user.is_superuser:
        courses = Course.objects.all()

    elif hasattr(user, 'teacher_profile'):
        teacher_profile = user.teacher_profile
        courses = Course.objects.filter(teacher=teacher_profile)
    
    elif hasattr(user, 'student_profile'):
        student_profile = user.student_profile
        courses = Course.objects.filter(enrollments__student=student_profile).distinct()

    return render(request, 'Courses/courses.html', {'courses': courses})

@login_required
@permission_required("study_managing.view_homework", raise_exception=True)
def homeworks_list(request):
    user = request.user
    submitted_ids = [] 
    
    now = timezone.now()
        
    if user.is_superuser:
        homeworks = Homework.objects.all().order_by(
            "-submission_date",
            "course__title",
        )

    elif hasattr(user, 'teacher_profile'):
        teacher_profile = user.teacher_profile
        homeworks = Homework.objects.filter(course__teacher__pk=teacher_profile.pk).order_by(
            "-submission_date",
            "course__title",
        )

    elif hasattr(user, 'student_profile'):
        student_profile = user.student_profile
        homeworks = Homework.objects.filter(course__enrollments__student=student_profile).distinct().order_by(
            "-submission_date",
            "course__title",
        )

        submitted_ids = SubmittedHomework.objects.filter(
            student=student_profile
        ).values_list("homework_id", flat=True)

    else:
        homeworks = Homework.objects.none()

    homeworks_with_status = []
    for homework in homeworks:
        homework.deadline_passed = now > homework.submission_date 
        homeworks_with_status.append(homework)

    return render(request, 'Homeworks/homeworks.html', {
        "homeworks": homeworks_with_status, 
        "submitted_ids": submitted_ids,
        "user": user
    })

    

@login_required
@permission_required("study_managing.view_enrollment", raise_exception=True)
def enrollments_list(request):
    user = request.user

    if hasattr(user, 'student_profile'):
        student_profile = user.student_profile
        enrollments = Enrollment.objects.filter(student = student_profile)

    elif hasattr(user, 'teacher_profile'):
        teacher_profile = user.teacher_profile
        enrollments = Enrollment.objects.filter(course__teacher = teacher_profile)

    elif user.is_superuser:
        enrollments = Enrollment.objects.all()
    return render(request, 'Enrollments/enrollments.html', {'enrollments': enrollments})

@login_required
@permission_required("study_managing.view_attendance", raise_exception=True)
def attendances_list(request):
    user = request.user
    attendances = Attendance.objects.none()

    if user.is_superuser:
        attendances = Attendance.objects.all().order_by(
            "enrollment__course__title",
            "enrollment__student__name",
            "-date"
        )

    elif hasattr(user, 'teacher_profile'):
        teacher_profile = user.teacher_profile
        attendances = Attendance.objects.filter(enrollment__course__teacher = teacher_profile).order_by(
            "enrollment__course__title",
            "enrollment__student__name",
            "-date"
        )

    elif hasattr(user, 'student_profile'):
        student_profile = user.student_profile
        attendances = Attendance.objects.filter(enrollment__student = student_profile).order_by(
            "enrollment__course__title",
            "enrollment__student__name",
            "-date"
        )
    return render(request, 'Attendances/attendances.html', {'attendances': attendances})

@login_required
@permission_required("study_managing.view_submittedhomework", raise_exception=True)
def submitted_homeworks_list(request):
    user = request.user
    if hasattr(user, 'student_profile'):
        student_profile = user.student_profile
        submittedHomeworks = SubmittedHomework.objects.filter(student = student_profile).order_by(
            "homework__course__title",
            "-submitted_at"
        )
    elif hasattr(user, 'teacher_profile'):
        teacher_profile = user.teacher_profile
        submittedHomeworks = SubmittedHomework.objects.filter(homework__course__teacher = teacher_profile).order_by(
            "homework__course__title",
            "student__name",
            "-submitted_at"
        )
    elif hasattr(user, 'teacher_profile') or user.is_superuser:
        submittedHomeworks = SubmittedHomework.objects.all().order_by(
            "homework__course__title",
            "student__name",
            "-submitted_at"
        )
    return render(request, 'SubmittedHomeworks/submittedHomeworks.html', {'submittedHomeworks': submittedHomeworks})

#Details view for homeworks and submitted homeworks because some text was not visible
@permission_required('study_managing.view_homework', raise_exception=True)
def homework_details(request, pk):
    homework = get_object_or_404(Homework.objects.select_related('course', 'course__teacher__user'), pk=pk)
    return render(request, 'Homeworks/homework_details.html', {
        'homework': homework,
})

@permission_required('study_managing.view_submittedhomework', raise_exception=True)
def submittedHomework_details(request, pk):
    submission = get_object_or_404(SubmittedHomework.objects.select_related('homework', 'homework__course__teacher__user'), pk=pk)
    return render(request, 'SubmittedHomeworks/submittedHomework_details.html', {
        'submission': submission,
})
#Create, Update, Delete views for students
@login_required
@permission_required("study_managing.add_student", raise_exception=True)
def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student was created successfully.")
            return redirect('students')
    else:
        form = StudentForm()
    return render(request, 'Students/create_student.html', {'form': form})

@login_required
@permission_required("study_managing.change_student", raise_exception=True)
def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance = student)
    if form.is_valid():
        form.save()
        messages.info(request, "Student was updated successfully.")
        return redirect('students')
    return render(request, 'Students/update_student.html', {'form': form})

@login_required
@permission_required("study_managing.delete_student", raise_exception=True)
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        messages.warning(request, "Student was deleted.")
        return redirect('students')
    return render(request, 'Students/delete_student.html', {'student': student})


#Create, Update, Delete views for teachers
@login_required
@permission_required("study_managing.add_teacher", raise_exception=True)
def create_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher was created successfully.")
            return redirect('teachers')
    else:
        form = TeacherForm()
    return render(request, 'Teachers/create_teacher.html', {'form': form})

@login_required
@permission_required("study_managing.change_teacher", raise_exception=True)
def update_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    form = TeacherForm(request.POST or None, instance = teacher)
    if form.is_valid():
        form.save()
        messages.info(request, "Teacher was updated successfully.")
        return redirect('teachers')
    return render(request, 'Teachers/update_teacher.html', {'form': form})

@login_required
@permission_required("study_managing.delete_teacher", raise_exception=True)
def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == "POST":
        teacher.delete()
        messages.warning(request, "Teacher was deleted.")
        return redirect('teachers')
    return render(request, 'Teachers/delete_teacher.html', {'teacher': teacher})


#Create, Update, Delete views for courses
@login_required
@permission_required("study_managing.add_course", raise_exception=True)
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course was created successfully.")
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'Courses/create_course.html', {'form': form})

@login_required
@permission_required("study_managing.change_course", raise_exception=True)
def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    form = CourseForm(request.POST or None, instance = course)
    if form.is_valid():
        form.save()
        messages.info(request, "Course was updated successfully.")
        return redirect('courses')
    return render(request, 'Courses/update_course.html', {'form': form})

@login_required
@permission_required("study_managing.delete_course", raise_exception=True)
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        course.delete()
        messages.warning(request, "Course was deleted.")
        return redirect('courses')
    return render(request, 'Courses/delete_course.html', {'course': course})


#CUD for enrollments
class EnrollmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'Enrollments/create_enrollment.html'
    success_url = reverse_lazy('enrollments')
    permission_required = ('study_managing.add_enrollment')

    def form_valid(self, form):
        messages.success(self.request, "Student was successfully enrolled!")
        return super().form_valid(form)

class EnrollmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'Enrollments/delete_enrollment.html'
    success_url = reverse_lazy('enrollments')
    permission_required = ('study_managing.delete_enrollment')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Enrollment record was successfully deleted!")
        return super().delete(request, *args, **kwargs)
    
#CU for attendances
class AttendanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'Attendances/create_attendance.html'
    success_url = reverse_lazy('attendances')
    permission_required = ('study_managing.add_attendance')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if hasattr(self.request.user, 'teacher_profile'):
            kwargs['teacher_profile'] = self.request.user.teacher_profile
        
        else:
            kwargs['teacher_profile'] = None

        return kwargs

class AttendanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'Attendances/update_attendance.html'
    success_url = reverse_lazy('attendances')
    permission_required = ('study_managing.change_attendance')


#CUD for homeworks
class HomeworkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'Homeworks/create_homework.html'
    success_url = reverse_lazy('homeworks')
    permission_required = ('study_managing.add_homework')
    def form_valid(self, form):
        messages.success(self.request, "Homework successfully created!")
        return super().form_valid(form)

class HomeworkUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'Homeworks/update_homework.html'
    success_url = reverse_lazy('homeworks')
    permission_required = ('study_managing.change_homework')
    def form_valid(self, form):
        messages.info(self.request, "Homework was updated")
        return super().form_valid(form)

class HomeworkDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'Homeworks/delete_homework.html'
    success_url = reverse_lazy('homeworks')
    permission_required = ('study_managing.delete_homework')
    def form_valid(self, form):
        messages.warning(self.request, "Homework was deleted")
        return super().form_valid(form)
    
#Views for submitted homework, submit= create submitted homework
@login_required
def submit_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    student = request.user.student_profile
    submission = SubmittedHomework.objects.filter(homework=homework, student=student).first()

    now = timezone.now()
    aware_deadline = homework.submission_date.astimezone(UTC)
    deadline_passed = now.astimezone(UTC) > aware_deadline

    if request.method == 'POST':
        if deadline_passed:
            messages.error(request, "Submission failed: The deadline for this homework has passed.")
            return redirect('homeworks') 
        
        form = SubmittedHomeworkStudentForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submitted = form.save(commit=False)
            submitted.student = student
            submitted.homework = homework
            submitted.save()
            messages.success(request, "Homework was successfully submitted!")
            return redirect('homeworks')
    
    else: #
        form = SubmittedHomeworkStudentForm(instance=submission)

    return render(request, 'SubmittedHomeworks/submit_homework.html', {
        'form': form,
        'homework': homework,
        'submission': submission,
        'deadline_passed': deadline_passed 
    })

@login_required
def delete_submittedHomework(request, submission_id):
    submission = get_object_or_404(SubmittedHomework, id=submission_id)
    
    if submission.grade is not None:
        messages.warning(request, "You cannot delete an already marked homework")
        return redirect("submitted_homeworks")
    
    if request.method == "POST":
        submission.delete()
        messages.success(request, "Submitted homework was successfully deleted")
        return redirect("submitted_homeworks")

    return render(request, "SubmittedHomeworks/delete_submittedHomework.html", {"submission": submission})

@login_required
def grade_homework(request, submission_id):
    submission = get_object_or_404(SubmittedHomework, id=submission_id)
    can_grade = (
        request.user.is_superuser or (hasattr(request.user, 'teacher_profile') and submission.homework.course.teacher == request.user.teacher_profile)
    )

    if not can_grade:
        messages.error(request, "You cannot grade this homework.")
        return redirect('submitted_homeworks')
    
    if request.method == 'POST':
        form = SubmittedHomeworkTeacherForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Homework was graded successfully!")
            return redirect('submitted_homeworks')
    else:
        form = SubmittedHomeworkTeacherForm(instance=submission)

    return render(request, 'SubmittedHomeworks/grade_homework.html', {'form': form, 'submission': submission})