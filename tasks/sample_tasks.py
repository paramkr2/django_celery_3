import time

from celery import shared_task
from .generate_data import run
from .load_data import load
@shared_task
def create_task(task_type):
	print(f'Task Started')
	if(int(task_type) == 1 ):
		print(f'Loading Data')
		res = load()
	else:
		print(f'Generating Data')
		res = run()
		
	return res 