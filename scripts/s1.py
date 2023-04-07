import datetime 
import pytz
def getoffset(x):
	datetime.datetime.now(pytz.timezone(x)).strftime('%z')
	res = pytz.timezone(x).localize(datetime.datetime(2011,1,1)).strftime('%z')
	inmin = int(res[:3])*60 + int( res[0] + res[3:] )
	return  inmin


res= getoffset('Asia/Tokyo')
print(res)
x = datetime.datetime(2010, 10, 31, 2, 12, 30)
y = x+ datetime.timedelta( minutes = 1 )*res
print(f'x:{x} y:{y}')