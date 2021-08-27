"""This module scans for assignments on viggo using beautifulsoup4 and the POST method"""
import re
import configparser
from requests import Session
# from bs4 import BeautifulSoup as bs

def lektiescan(output):
    """Function that scans assignments then returns each element in a dict"""
    config = configparser.ConfigParser()
    config.read('cred.ini')
    if output is True:
        print('lektiescanning...')
    user_name = config['config']['USERNAME']
    password = config['config']['PASSWORD']
    fingerprint = config['config']['FINGERPRINT']
    with Session() as s: # pylint: disable=invalid-name
        login_data = {"UserName": user_name, "Password": password, "fingerprint": fingerprint}
        s.post("https://nr-aadal.viggo.dk/Basic/Account/Login", login_data)
        home_page = s.get("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment")
        home_page = str(home_page.content).replace('\\n', '\n').replace('\\r', '\r').replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xa5', 'å').replace('&#xF8;', 'ø').replace('&#xE5;', 'å').replace('\\xc3\\xa6', 'æ').replace('\\xc3\\x98', 'Ø')
        links = re.findall("(?<=<a href=\"/Basic/HomeworkAndAssignment/Details/).*?(?=/#modal)", home_page)
        begivenhed = []
        tidspunkt = []
        beskrivelse = []
        author = []
        files = []
        file_names = []
        url = []
        for i in enumerate(links):
            i = i[0]
            home_page = s.get("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment/Details/" + links[i] + "/#modal")
            url.append("https://nr-aadal.viggo.dk/Basic/HomeworkAndAssignment/Details/" + links[i] + "/#modal")
            home_page = str(home_page.content).replace('\\n', '\n').replace('\\r', '\r').replace('\\xc3\\xb8', 'ø').replace('\\xc3\\xa5', 'å').replace('&#xF8;', 'ø').replace('&#xE5;', 'å').replace('\\xc3\\xa6', 'æ').replace('\\xc3\\x98', 'Ø').replace('&nbsp;', '')
            new_subject = re.findall("(?<=class=\"ajaxModal\">).*?(?=</a>)", home_page)
            begivenhed.append(new_subject[0].replace('&#xE6;', 'æ'))
            new_time = re.findall("(?<=<dd>).*?(?= <)", home_page)
            tidspunkt.append(new_time[0])
            new_description = re.findall("(?<=<div class=\"content\">).*?(?=</div>)", home_page)
            link_in_post = ''
            if "\" rel=\"noopener noreferrer\" target=\"_blank\">" in new_description[0]:
                link_in_post = re.findall("(?<=\" rel=\"noopener noreferrer\" target=\"_blank\">).*?(?=</a>)", new_description[0])[0]
            double_link = link_in_post + link_in_post
            pre_hex_removal = new_description[0].replace('<p>', '\n').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').replace('<br>', '').replace('<a href=\"', '').replace('\" rel=\"noopener noreferrer\" target=\"_blank\">', '').replace('</a>', '').replace(double_link, link_in_post)
            pre_hex_removal = pre_hex_removal.replace('\\x', '|')
            hex_to_remove = re.findall("(?<=|).*?(?= |\n)", pre_hex_removal) ##########IMPORTANT!!!! place backslash before the first pipe if the function isnt working
            for j in enumerate(hex_to_remove):
                j = j[0]
                replacements = hex_to_remove[j]
                pre_hex_removal = pre_hex_removal.replace(replacements, '')
            finished_description = pre_hex_removal.replace('|', '')
            new_author = re.findall("(?<=<p><small class=\"muted\">).*?(?=</small></p>)", home_page)
            author.append(new_author[0])
            new_file = re.findall("(?<=<a class=\"ajaxModal\" href=\").*?(?=\")", home_page)
            if len(new_file) != 0:
                for j in enumerate(new_file):
                    j = j[0]
                    new_file[j] = "https://nr-aadal.viggo.dk" + new_file[j]
                file_collection = str(new_file).replace('[', '').replace(']', '').replace('\'', '')
            else:
                file_collection = "None"
            files.append(file_collection)
            fnew_file_name = re.findall("(?<=<span>).*?(?=</span>)", home_page)
            if len(fnew_file_name) != 0:
                for j in enumerate(fnew_file_name):
                    j = j[0]
                    fnew_file_name[j] = fnew_file_name[j].replace('&#xE6;', 'æ')
                file_name_collection = str(fnew_file_name).replace('[', '').replace(']', '').replace('\'', '')
            else:
                file_name_collection = "None"
            file_names.append(file_name_collection)
            if link_in_post != '':
                target = re.findall("(?<=\" rel=\"noopener noreferrer\" target=\"_blank\">).*?(?=</a>)", new_description[0])
                href = re.findall("(?<=<a href=\").*?(?=\")", new_description[0])
                for j in enumerate(href):
                    j = j[0]
                    if target[j] != href[j]:
                        finished_description = finished_description.replace(target[j], '')
                        finished_description = finished_description.replace(href[j], f"[{target[i]}]({href[i]})")
            beskrivelse.append(finished_description)

    return {
        'begivenhed': begivenhed,
        'beskrivelse': beskrivelse,
        'author': author,
        'files': files,
        'tidspunkt': tidspunkt,
        'file_names': file_names,
        'url': url
    }
