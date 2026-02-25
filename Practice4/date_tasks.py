from datetime import datetime , timedelta , timezone
#1.five days from current date 
today=datetime.now()
five_days_ago=today-timedelta(days=5)
print("Five days ago: ",five_days_ago)

#2.yesterday,today,tomorrow
yesterday=today-timedelta(days=1)
tomorrow=today+timedelta(days=1)

print("Yesterday: ",yesterday.date())
print("Today: ",today.date())
print("Tomorrow: ",tomorrow.date())

#3.drop microsecond
without_microsecond=today.replace(microsecond=0)
print("Without microsecond: ",without_microsecond)

#4.difference in seconds
date1=datetime(2024,1,1)
date2=datetime(2024,1,2)

difference=date2-date1
print("Difference in seconds: ",difference.total_seconds())