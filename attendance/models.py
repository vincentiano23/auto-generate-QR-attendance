from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.registration_number

class Unit(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.registration_number} - {self.unit.name} - {'Present' if self.is_present else 'Absent'}"


class QRCode(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    qr_code_image = models.ImageField(upload_to='qrcodes/')

    def save(self, *args, **kwargs):

        qr_img = qrcode.make(self.student.registration_number)


        buffer = BytesIO()
        qr_img.save(buffer, 'PNG')
        buffer.seek(0) 

        fname = f'qrcodes/{self.student.registration_number}.png'
        self.qr_code_image.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"QR Code for {self.student.user.get_full_name()}"
