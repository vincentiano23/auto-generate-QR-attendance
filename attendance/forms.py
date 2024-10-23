from django import forms
from .models import Department, Student, QRCode
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizing the form fields for Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)  # Make required=True for better validation
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)

    class Meta:
        model = Student
        fields = ['registration_number', 'course', 'department']  # Include department in the fields

    def save(self, commit=True):
        # Create the user instance
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        # Create the student instance without saving it yet
        student = super().save(commit=False)
        student.user = user  # Link the created user to the student
        if commit:
            student.save()  # Save the student instance
            QRCode.objects.create(student=student)  # Generate the QR code for the student
        return student

class ScanQRCodeForm(forms.Form):
    qr_code = forms.CharField(label="Scan QR Code")
    unit_id = forms.IntegerField(widget=forms.HiddenInput())

class CustomUserCreationForm(UserCreationForm):
    registration_number = forms.CharField(max_length=100, label="Registration Number", required=True)  # Added required=True
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", required=True)  # Added required=True
    course = forms.CharField(max_length=100, label="Course", required=True)  # Added required=True

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'registration_number', 'department', 'course']
