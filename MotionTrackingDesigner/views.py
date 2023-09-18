from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from .forms import CameraForm
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.views.decorators import gzip
from django.conf import settings
from rest_framework.views import APIView
import cv2, time, os
from .models import Camera, Rectangle


class IndexView(TemplateView):
    template_name = 'index.html'

class AdjustReferance(View):
    def get(self, request):
        # Referans ayarlama işlemleri
        return render(request, 'adjust_referance.html')

class Config(View):
    template_name = 'config.html'
    def get(self, request):
        camera = Camera.objects.first()
        form = CameraForm(instance=camera)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        camera = Camera.objects.first()
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            form.save()
        # return render(request, self.template_name, {'form': form})
        return redirect("/referans-ayarlama/")

class SettingsInfo(View):
    template_name = 'index.html'

class AddImage(View):
    def get(self, request):
        return render(request, 'add_image.html')

    def post(self, request):
        if request.FILES.getlist('images'):
            for image in request.FILES.getlist('images'):
                save_path = os.path.join(settings.MEDIA_ROOT, image.name)
                with open(save_path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                # İşlemleriniz burada devam edebilir...
        return render(request, 'add_image.html')

class FlowPlanning(View):
    def get(self, request):
        # Akış Planlama işlemleri
        return render(request, 'flow_planning.html')

# Kamera görüntüsünü elde etmek için kullanılacak yardımcı sınıf
class CameraStream:
    def __init__(self):
        camera = Camera.objects.first()  # İlk kamera verisini alır, gerekirse sorguyu güncelleyin
        username = camera.username
        password = camera.password
        camera_ip = camera.camera_ip
        self.video_capture = cv2.VideoCapture(f"rtsp://{username}:{password}@{camera_ip}/cam/realmonitor?channel=1@subtype=0")

    def __iter__(self):
        while True:
            success, frame = self.video_capture.read()
            if not success:
                break

            # Görüntüyü JPEG formatına dönüştürme
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()

            # İteratör olarak görüntüyü döndürme
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    def release(self):
        self.video_capture.release()

class CameraFeedView(APIView):
    def get(self, request):
        try:
            return StreamingHttpResponse(CameraStream(), content_type='multipart/x-mixed-replace; boundary=frame')
        except GeneratorExit:
            return None

class SaveRectangleView(View):
    def post(self, request):
        if "xmin" in request.POST and "ymin" in request.POST and "xmax" in request.POST and "ymax" in request.POST:
            xmin = int(request.POST["xmin"])
            ymin = int(request.POST["ymin"])
            xmax = int(request.POST["xmax"])
            ymax = int(request.POST["ymax"])
            rectangle = Rectangle(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
            rectangle.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "Invalid request"})

