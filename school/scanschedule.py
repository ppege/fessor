import schedule
import time
from lektiescanner import lektiescan

def scan():
    beskrivelse, begivenhed, tidspunkt, files, fileNames, author = lektiescan()
    f = open("scanResults.txt", "r")
    previousResults = f.read()
    f.close()
    if str(begivenhed) == previousResults:
    	return
    else:
    	f = open("scanResults.txt", "w")
    	f.write(str(begivenhed))
    	f.close
    	

schedule.every(20).minutes.do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)