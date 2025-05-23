from django.urls import path
from . import views

urlpatterns = [
    path('', views.fileUploadIndex),
    path('file_upload', views.fileUpload),
    path('mail_summary', views.sendMailWithSummary),
    path('download_filtered', views.downloadFilteredFile),
    path('delete_filtered', views.deleteFilteredFile)
]