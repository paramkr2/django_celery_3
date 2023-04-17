
import csv
from tasks.models import StoreStatus,BusinessHours,StoreTimezone
from itertools import islice
from collections import Counter,defaultdict
from django.db import models 
from datetime import datetime, timezone,timedelta,time
from dateutil import tz
import numpy as np
from scipy import interpolate
import math
import pandas as pd
from django_thread import Thread
import string
import random
import pytz	
from django.db.models import F	,OuterRef, Subquery
from django.db.models.functions import Coalesce,Cast

def to_hm_int(time):
	# convert hh:mm:ss into hour*60+min.. or just total minutes 
	return int(str(time)[:2])*60 + int(str(time)[3:5])

def get_day_uptime(id,day_entries ):
	time_list = []
	status_list = []
	day = 0
	for row in day_entries:
		date_time = str(row['datetime_local'])[:-2] 
		time_list.append( to_hm_int ( str(row['datetime_local'])[11:16] ) )
		status_list.append( 1 if row['status'] =='active' else 0 );
		
	
	# Get business hours time range 

	start_time , end_time = to_hm_int(day_entries[0]['start_time']) , to_hm_int( day_entries[0]['end_time'] )
	full_time = np.arange(start_time,end_time,1)
	ip_func = interpolate.interp1d(time_list, status_list ,kind='nearest',fill_value="extrapolate")
	new_status_list = ip_func(full_time)
	
	return new_status_list,start_time,end_time

def get_results(id,week_list):

	dates = list( week_list.keys() )
	dates.sort(reverse=True)
	week_uptime,week_downtime=0,0
	day_uptime,day_downtime=0,0
	hour_uptime,hour_downtime = 0,0 	
	for i,date in enumerate(dates ):
		lis,st,et = get_day_uptime( id ,week_list[date] ) 
		if( i == 0 ):
			# generate day and hour result 
			day_uptime = sum(lis) 
			day_downtime = (et-st) - day_uptime 
			day_uptime //= 60
			day_downtime //= 60
			hour_uptime = math.floor( sum(lis[:60]) )
			hour_downtime = math.floor( 60-hour_uptime )
		else:
			t1 = sum(lis) 
			t2 = (et-st) - day_uptime 
			t1 //= 60
			t2 //= 60
			week_uptime += t1
			week_downtime += t2
	return hour_uptime,day_uptime,week_uptime,hour_downtime,day_downtime,week_downtime


def randomstring(n):
	return  ''.join(random.choices(string.ascii_letters, k=n))
	

def run():
	# Attach offset alias to storesttus 
	y = StoreStatus.objects.all().annotate( 
		offset =  Cast( 
			timedelta(minutes=1)* \
			Coalesce( 
				Subquery( 
					StoreTimezone.objects.filter(storeid=OuterRef('storeid')) .values('utcoffset')[:1] 
				),-5*60
			)  , output_field=models.DurationField()
		)
	)
	
	# update with offset value to local time 
	y.all().update(datetime_local = F('datetime_utc') + F('offset') ) 
	
	print(f'Converted to local time')
	
	# get the start and end time 
	x = StoreStatus.objects.all().annotate( 
		start_time = Cast( Coalesce( Subquery(
			BusinessHours.objects.filter( 
				storeid = OuterRef('storeid') , dayofweek=OuterRef('datetime_local__week_day') 
			).values('start_time')[:1]  
		),time(0,0,0) ), output_field=models.TimeField() ),
		end_time = Cast( Coalesce( Subquery(
			BusinessHours.objects.filter( 
				storeid = OuterRef('storeid') , dayofweek=OuterRef('datetime_local__week_day') 
			).values('end_time')[:1]  
		),time(23,59,59)), output_field=models.TimeField() ),
		dayofweek = F('datetime_local__week_day') 
	) 
		
	print(f'annoted object is x ')
	
	ids = StoreStatus.objects.order_by().values_list('storeid',flat=True ).distinct()
	today = datetime(23,1,27,12,12,12)
	
	final_list =  [['store_id', 'uptime_last_hour', 'uptime_last_day','update_last_week', \
		'downtime_last_hour', 'downtime_last_day', 'downtime_last_week' ] ]
	for i,id in enumerate(ids):
		week_list = x.all().order_by('storeid').filter(
			storeid=id , datetime_local__gte = today - timedelta(days=7) 
		).values_list( 'storeid','datetime_local','start_time','end_time' , 'dayofweek','status')
		
		#populate for each day 
		hmap = defaultdict(list)
		for item in week_list:
			date = str(item[1])[:10]
			item_dict = { 'storeid':item[0],'datetime_local':item[1],'start_time':item[2],'end_time':item[3] , 'dayofweek':item[4],'status' :item[5] }
			hmap[date].append( item_dict ) 
		#print(hmap.keys())
		res = get_results( int(id), hmap ) 
		final_list.append( [id] +  list(res) )
		if(i%1000==0): print(f' Completed:{i}')

	df = pd.DataFrame(final_list)
	x = 'res' + randomstring(10) +'.csv'
	path = str( 'static/' + x  )
	
	df.to_csv(path, index=False,encoding='utf-8')
	print(df.head())
	print(df.dtypes)

	return 'staticfiles/' + x 	
	
	