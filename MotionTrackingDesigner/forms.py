from django import forms
from .models import Camera

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ('camera_ip', 'username', 'password')
        widgets = {
            'password': forms.PasswordInput()  # Şifre alanını gizli yapmak için PasswordInput widget'ı kullanılır.
        }