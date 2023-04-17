from django.db import models


class StoreStatus(models.Model):
	storeid = models.CharField(max_length=150)
	datetime_utc = models.DateTimeField(auto_now=False, auto_now_add=False)
	datetime_local = models.DateTimeField(auto_now=True)
	datetime_temp = models.DateTimeField(auto_now=True)
	#time_utc = models.TimeField(auto_now=True)
	status = models.CharField(max_length=150)
	class Meta:
		indexes = [
			models.Index(fields=['storeid'])
		]
	def __str__(self):
		return self.storeid
		
class BusinessHours(models.Model):
	storeid = models.CharField(max_length=150)
	dayofweek = models.IntegerField(null=True)
	start_time = models.TimeField(auto_now=False)
	end_time = models.TimeField(auto_now=False)
	class Meta:
		indexes = [
			models.Index(fields=['storeid'])
		]
	def __str__(self):
		return self.storeid 
		
class StoreTimezone(models.Model):
	storeid = models.CharField(max_length=150 , unique=True)
	timezone = models.CharField(max_length=150)
	utcoffset = models.IntegerField( default=-500 )
	class Meta:
		indexes = [
			models.Index(fields=['storeid'])
		]
	def __str__(self):
		return self.storeid
	