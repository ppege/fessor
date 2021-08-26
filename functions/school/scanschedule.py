import schedule
import time
from lektiescanner import lektiescan
from lektieposter import post

print('scan schedule started')

def scan():
    print('scan() called')
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
    	post(begivenhed, beskrivelse, author, files, tidspunkt, fileNames)

schedule.every(20).seconds.do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)