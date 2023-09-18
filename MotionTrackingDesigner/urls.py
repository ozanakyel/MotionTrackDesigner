from django.urls import path
from .views import IndexView, FlowPlanning, AddImage, Config, AdjustReferance, CameraFeedView, SaveRectangleView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('config/', Config.as_view(), name='config'),
    path('referans-ayarlama/', AdjustReferance.as_view(), name='referans-ayarlama'),
    path('fotograf-ekleme/', AddImage.as_view(), name='fotograf-ekleme'),
    path('akis-planlama/', FlowPlanning.as_view(), name='akis-planlama'),
    path('api/SettingsInfo', FlowPlanning.as_view(), name='akis-planlama'),
    path('camera_feed/', CameraFeedView.as_view(), name='camera_feed'),
    path('save_rectangle/', SaveRectangleView.as_view(), name='save_rectangle'),
    ]
