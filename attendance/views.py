from django.shortcuts import redirect, render, get_object_or_404
from .models import Attendance, Student, QRCode, Unit
from django.http import HttpResponse
from .forms import StudentRegistrationForm, CustomUserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    try:
        student = request.user.student  # Attempt to get the student's profile
        qr_code = get_object_or_404(QRCode, student=student)
        context = {'qr_code': qr_code}
    except Student.DoesNotExist:
        messages.error(request, 'You are not registered as a student. Please contact the administrator.')
        return redirect('register_student')  # Redirect to registration page or handle as needed

    return render(request, 'home.html', context)

def login_view(request):
    return render(request, 'registration/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in automatically after registration
            
            messages.success(request, f'Account created successfully! You are now logged in as {user.username}')
            return redirect('home')  # Redirect to the homepage after successful login
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to the login page

@login_required
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the student and create the QR code if necessary
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('registration_success')  # Redirect to a success page after registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'attendance/registration.html', {'form': form})

def registration_success(request):
    return render(request, 'attendance/registration_success.html')

def generate_qr_code(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    qr_code, created = QRCode.objects.get_or_create(student=student)
    return render(request, 'qr_code.html', {'qr_code': qr_code})

def scan_qr_code(request, qr_code):
    try:
        student = Student.objects.get(registration_number=qr_code)
        unit_id = request.POST.get('unit_id')
        if not unit_id:
            return HttpResponse('Unit ID not provided.', status=400)

        unit = get_object_or_404(Unit, id=unit_id)

        # Create an attendance record marking the student as present
        Attendance.objects.create(student=student, unit=unit, is_present=True)

        return HttpResponse('Attendance marked successfully.')

    except Student.DoesNotExist:
        return HttpResponse('Invalid QR code.', status=404)

@login_required
def attendance_stats(request):
    students = Student.objects.all()
    stats = []
    for student in students:
        total_classes = Attendance.objects.filter(student=student).count()
        attended_classes = Attendance.objects.filter(student=student, is_present=True).count()
        attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        stats.append({'student': student, 'attendance_percentage': attendance_percentage})

    return render(request, 'attendance/attendance_stats.html', {'stats': stats})
