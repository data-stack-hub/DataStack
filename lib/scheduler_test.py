import datastack as ds
from apscheduler.schedulers.background import BackgroundScheduler
import test_app

ds.header('Scheduler')

def task():
    print('This is test task')
    ds.header('this is test task')

scheduler = BackgroundScheduler()
scheduler.add_job(task,'interval', seconds = 2)
scheduler.start()
