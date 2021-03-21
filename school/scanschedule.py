import schedule
import time
import lektiescanner

def job():
    lektescanner.lektiescan()

schedule.every(20).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)