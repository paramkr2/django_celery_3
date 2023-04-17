from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tasks.sample_tasks import create_task
from celery.result import AsyncResult
from django.http import FileResponse
import os

def home(request):
    return render(request, "home.html")


@csrf_exempt
def trigger_report(request):
	if request.POST:
		task_type = request.POST.get("type")
		task = create_task.delay(int(task_type))
		return JsonResponse({"task_id": task.id}, status=202)


@csrf_exempt
def get_report(request, task_id):
	task_result = AsyncResult(task_id)
	result = {
		"task_id": task_id,
		"task_status": 'Running' if task_result.status == 'Pending' else task_result.status ,
		"task_result": task_result.result
	}
	if request.POST :
		return JsonResponse(result, status=202)
	return JsonResponse(result, status=200)
	
def download_csv(request,filename):
	
	file_path = pwd = os.path.dirname(__file__) + f'/../csv/{filename}'
	file = open(file_path, 'rb')
	response = FileResponse(file)
	return response
