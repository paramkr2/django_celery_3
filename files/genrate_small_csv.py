import pandas as pd 

df_timezone = pd.read_csv('store_timezone_base.csv');
df_business_hours = pd.read_csv('business_hours_base.csv');
df_store_status = pd.read_csv('store_status_base.csv');

store_ids = df_timezone['store_id'][:1000]

# here code insice [] also generates a mask, which we use to filter out the rows 
df_timezone = df_timezone[ df_timezone.store_id.isin(store_ids) ]
df_business_hours = df_business_hours[ df_business_hours.store_id.isin(store_ids) ]
df_store_status = df_store_status[ df_store_status.store_id.isin(store_ids) ]
		
print(f'df_store_status:{ len(df_store_status)}  df_timezone:{len(df_timezone)} df_business_hours:{ len(df_business_hours)} ')



df_timezone.to_csv('store_timezone.csv',index=False)
df_business_hours.to_csv('business_hours.csv',index=False)
