from django.contrib import admin
from django.urls import path
from tasks.views import get_report, home, trigger_report , download_csv


urlpatterns = [
    path("admin/", admin.site.urls),
	path("", home, name="home"),
    path("get_report/<task_id>/", get_report, name="get_report"),
    path("trigger_report/", trigger_report, name="trigger_report"),
	path("csv/<str:filename>/",download_csv,name="download_csv"),
    
] 

