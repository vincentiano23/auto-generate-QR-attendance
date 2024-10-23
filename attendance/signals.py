from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, QRCode
import qrcode
from io import BytesIO
from django.core.files import File

@receiver(post_save, sender=Student)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        # Check if QRCode already exists for this student
        qr_code, created = QRCode.objects.get_or_create(student=instance)

        if not created:
            # QR code already exists, you can handle this case if needed
            return

        # Create a QR code for the student's registration number
        qr_img = qrcode.make(instance.registration_number)
        
        # Define the filename and save path for the QR code image
        fname = f'qrcodes/{instance.registration_number}.png'

        # Save the QR code image to a BytesIO buffer
        buffer = BytesIO()
        qr_img.save(buffer, 'PNG')
        buffer.seek(0)  # Ensure the pointer is at the start of the buffer

        # Save the QR code image to the QRCode instance
        qr_code.qr_code_image.save(fname, File(buffer), save=False)
        qr_code.save()  # Save the QRCode instance