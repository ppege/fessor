from requests import Session
from bs4 import BeautifulSoup as bs
import re
import os
import file

UserName = os.getenv('USERNAME')
Password = os.getenv('PASSWORD')
fingerprint = os.getenv('FINGERPRINT')

def lektiescan():
  print('lektiescanning...')



  with Session() as s:
    site = s.get("https://nr-aadal.viggo.dk/Basic/Account/Login")
    bs_content = bs(site.content, "html.parser")
    login_data = {"UserName": UserName, "Password": Password, "fingerprint": fingerprint}
    s.post("https://nr-aadal.viggo.dk/Basic/Account/Login", login_data)
    home_page = s.get("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment")
    home_page = str(home_page.content).replace('\\n', '\n').replace('\\r', '\r').replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xa5', 'å').replace('&#xF8;', 'ø').replace('&#xE5;', 'å').replace('\\xc3\\xa6', 'æ').replace('\\xc3\\x98', 'Ø')
    links = re.findall("(?<=<a href=\"/Basic/HomeworkAndAssignment/Details/).*?(?=/#modal)", home_page)
    begivenhed = []
    tidspunkt = []
    beskrivelse = []
    author = []
    files = []
    fileNames = []
    print('post-clear: ' + str(begivenhed))
    for i in range(0, len(links)):
        home_page = s.get("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment/Details/" + links[i] + "/#modal")
        home_page = str(home_page.content).replace('\\n', '\n').replace('\\r', '\r').replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xa5', 'å').replace('&#xF8;', 'ø').replace('&#xE5;', 'å').replace('\\xc3\\xa6', 'æ').replace('\\xc3\\x98', 'Ø')
        newBegivenhed = re.findall("(?<=class=\"ajaxModal\">).*?(?=</a>)", home_page)
        begivenhed.append(newBegivenhed[0].replace('&#xE6;', 'æ'))
        newTidspunkt = re.findall("(?<=<dd>).*?(?= <)", home_page)
        tidspunkt.append(newTidspunkt[0])
        newBeskrivelse = re.findall("(?<=<div class=\"content\">).*?(?=</div>)", home_page)
        linkInPost = ''
        if "\" rel=\"noopener noreferrer\" target=\"_blank\">" in newBeskrivelse[0]:
            linkInPost = re.findall("(?<=\" rel=\"noopener noreferrer\" target=\"_blank\">).*?(?=</a>)", newBeskrivelse[0])[0]
        doubleLink = linkInPost + linkInPost
        preHexRemoval = newBeskrivelse[0].replace('<p>', '\n').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').replace('<br>', '').replace('<a href=\"', '').replace('\" rel=\"noopener noreferrer\" target=\"_blank\">', '').replace('</a>', '').replace(doubleLink, linkInPost)
        preHexRemoval = preHexRemoval.replace('\\x', '|')
        hexToRemove = re.findall("(?<=\|).*?(?= |\n)", preHexRemoval)
        for i in range(0, len(hexToRemove)):
          shitToReplaceInForLoop = hexToRemove[i]
          preHexRemoval = preHexRemoval.replace(shitToReplaceInForLoop, '')
        finishedBeskrivelse = preHexRemoval.replace('|', '')
        beskrivelse.append(finishedBeskrivelse)
        newAuthor = re.findall("(?<=<p><small class=\"muted\">).*?(?=</small></p>)", home_page)
        author.append(newAuthor[0])
        newFil = re.findall("(?<=<a class=\"ajaxModal\" href=\").*?(?=\")", home_page)
        if len(newFil) != 0:
          for i in range(0, len(newFil)):
            newFil[i] = "https://nr-aadal.viggo.dk" + newFil[i]
          fileCollection = str(newFil).replace('[', '').replace(']', '').replace('\'', '')
        else:
          fileCollection = "Ingen"
        files.append(fileCollection)
        newFileName = re.findall("(?<=<span>).*?(?=</span>)", home_page)
        if len(newFileName) != 0:
          for i in range(0, len(newFileName)):
            newFileName[i] = newFileName[i].replace('&#xE6;', 'æ')
          fileNameCollection = str(newFileName).replace('[', '').replace(']', '').replace('\'', '')
        else:
          fileNameCollection = "Ingen"
        fileNames.append(fileNameCollection)
  
  return begivenhed, tidspunkt, beskrivelse, author, files, fileNames