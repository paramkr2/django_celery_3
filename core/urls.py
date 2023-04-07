from django.contrib import admin
from django.urls import path

from tasks.views import get_report, home, trigger_report
from createmodels.views import create_model 
urlpatterns = [
    path("admin/", admin.site.urls),
    path("get_report/<task_id>/", get_report, name="get_report"),
    path("trigger_report/", trigger_report, name="trigger_report"),
	path("createmodels/",create_model,name="create_model"),
    path("", home, name="home"),
] 
