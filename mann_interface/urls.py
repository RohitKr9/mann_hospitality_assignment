from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.fileUploadIndex),
    path('file_upload', views.fileUpload),
    path('mail_summary', views.sendMailWithSummary)
]