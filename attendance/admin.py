from django.contrib import admin
from .models import Department, Lecturer, Student, Unit, Attendance, QRCode

admin.site.register(Department)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Unit)
admin.site.register(Attendance)
admin.site.register(QRCode)
