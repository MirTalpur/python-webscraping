from lxml import html
import requests
from selenium import webdriver
from datetime import datetime
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Note I use selenium to navigate to needed urls and interact with the webpage
# if this is not needed please let me know and I can make the needed changes required
# But I assumed the given URL in the project documentation was the only one you can go to
# directly and the rest of them required some sort of scripting
# For example I can directly go to https://www.occ.gov/topics/licensing/interpretations-and-actions/interpretations-and-actions-archive.html
# which has the entire achieve instead of the given starting link provided in the assignment and
# finding the metadata on that page becomes easy that way however I wanted the script to use the START
# URL and navigate to the needed information
# For webdriver I used selenium firefox for this you need firefox and geicko installed
# https://github.com/mozilla/geckodriver/releases
# I'm not sure which OS you are on so it's a bit different for each OS

# GamePlan:
# So essentially use selenium to get to where u want to go
# and than in order to get the data use lxml for the parsing and content in tree form
# but use request library to get the html content of the page

# Base URL is used for selenium webdriver to navigate to needed url
BASE_URL = "https://www.occ.gov"
# Start URL Provided in documentation for assignment
START_URL = "https://www.occ.gov/topics/licensing/interpretations-and-actions/index-interpretations-and-actions.html"
letter_no_topic_interpretive_letter = []
date_href_interpretive_letter = []
letter_no_topic_corporate_decisions = []
date_href_corporate_decisions = []
letter_no_topic_approvals_with_conditions_enforceable = []
date_href_approvals_with_conditions_enforceable = []
letter_no_topic_cra_decision = []
date_href_cra_decision = []

def output_to_csv():
    '''
    Output the data to a csv
    '''
    with open('filename.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(["Interpretations and Actions"])
        wr.writerow(('Letter No.', 'Topic','Date', 'href'))
        for i in range(0, len(letter_no_topic_interpretive_letter), 2):
            wr.writerow((letter_no_topic_interpretive_letter[i], letter_no_topic_interpretive_letter[i + 1], date_href_interpretive_letter[i], date_href_interpretive_letter[i+1]))
        wr.writerow(["Corporate Decisions"])
        wr.writerow(('Letter No.', 'Topic','Date', 'href'))
        for i in range(0, len(letter_no_topic_corporate_decisions), 2):
            wr.writerow((letter_no_topic_corporate_decisions[i], letter_no_topic_corporate_decisions[i + 1], date_href_corporate_decisions[i], date_href_corporate_decisions[i+1]))
        wr.writerow(["Approvals with Conditions Enforceable under 12 U.S.C. 1818"])
        wr.writerow(('Letter No.', 'Topic', 'Date', 'href'))
        for i in range(0, len(letter_no_topic_approvals_with_conditions_enforceable), 2):
            wr.writerow((letter_no_topic_approvals_with_conditions_enforceable[i], letter_no_topic_approvals_with_conditions_enforceable[i + 1], date_href_approvals_with_conditions_enforceable[i], date_href_approvals_with_conditions_enforceable[i+1]))
        wr.writerow(["CRA Decisions"])
        wr.writerow(('Letter No.', 'Topic', 'Date', 'href'))
        for i in range(0, len(letter_no_topic_cra_decision), 2):
            wr.writerow((letter_no_topic_cra_decision[i],
                         letter_no_topic_cra_decision[i + 1],
                         date_href_cra_decision[i],
                         date_href_cra_decision[i + 1]))

def get_common_table_data_march(path, type):
    '''
    get common table data from the march page
    essentially most of the data follows the same format at least on the march page
    '''
    table_data = tree.xpath(path + '//text()')
    while 'Topic' in table_data: table_data.remove('Topic')
    while '\n' in table_data: table_data.remove('\n')
    while '\n\n' in table_data: table_data.remove('\n\n')
    while 'Letter No.'in table_data: table_data.remove('Letter No.')
    while ' (PDF)' in table_data: table_data.remove(' (PDF)')
    for i in range(1,len(table_data),2):
        table_data[i] = ''.join([j if ord(j) < 128 else ' ' for j in table_data[i]])
    # add all of the date
    dates = []
    for i,value in enumerate(table_data[1::2]):
        match = re.search(r'\d{2}/\d{2}/\d{4}',value)
        date = datetime.strptime(match.group(), '%m/%d/%Y').date()
        dates.append(date.strftime('%m/%d/%Y'))
    ahref_interpretives = tree.xpath(path + '//a/@href')
    date_href = []
    for date,ahref_interpretive in zip(dates,ahref_interpretives):
        date_href.append(date)
        date_href.append(ahref_interpretive)
    # table_data.extend(ahref_interpretive)
    if type == 'interpretive':
        letter_no_topic_interpretive_letter.extend(table_data)
        date_href_interpretive_letter.extend(date_href)
    elif type == 'corporate':
        letter_no_topic_corporate_decisions.extend(table_data)
        date_href_corporate_decisions.extend(date_href)
    elif type == 'approvals':
        letter_no_topic_approvals_with_conditions_enforceable.extend(table_data)
        date_href_approvals_with_conditions_enforceable.extend(date_href)

def get_common_table_data_august(path,type):
    '''
    get the data from the august page
    '''
    table_data = tree.xpath(path + '//text()')
    while 'Topic' in table_data: table_data.remove('Topic')
    while '\n' in table_data: table_data.remove('\n')
    while '\n\n' in table_data: table_data.remove('\n\n')
    while 'Letter No.'in table_data: table_data.remove('Letter No.')
    while '\r\n' in table_data: table_data.remove('\r\n')
    while 'WORD' in table_data: table_data.remove('WORD')

    for i in range(len(table_data)):
        table_data[i] = ''.join([j if ord(j) < 128 else ' ' for j in table_data[i]])
    dates = []
    index_to_pop = []
    for i in range(len(table_data)-1):
        match = re.search(r'\d{2}/\d{2}/\d{4}', table_data[i])
        if match:
            dates.append(table_data[i])
            index_to_pop.append(i)

    for i in range(len(index_to_pop)):
        table_data.pop(index_to_pop[i])
    table_data_length = len(table_data)
    match_last_element = re.search(r'\d{2}/\d{2}/\d{4}', table_data[table_data_length-1])
    if match_last_element:
        table_data.pop(table_data_length-1)
    for i,value in enumerate(table_data):
        match = re.search(r'\d{2}/\d{2}/\d{4}',value)
        if match:
            date = datetime.strptime(match.group(), '%m/%d/%Y').date()
            dates.append(date.strftime('%m/%d/%Y'))
    # for i in range(3, len(table_data), 3):
    #     dates.append(table_data[i])
    #     table_data.pop(i)
    ahref_interpretives = tree.xpath(path + '//a/@href')
    date_href = []
    for date,ahref_interpretive in zip(dates,ahref_interpretives):
        date_href.append(date)
        date_href.append(ahref_interpretive)
    if type == 'interpretive':
        letter_no_topic_interpretive_letter.extend(table_data)
        date_href_interpretive_letter.extend(date_href)
    elif type == 'cra':
        letter_no_topic_cra_decision.extend(table_data)
        date_href_cra_decision.extend(date_href)

def get_august_interpretive_letters(tree):
    letter_no_data = []
    letter_no_data.extend(tree.xpath('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]/tr[2]/td[1]' + '//text()'))
    letter_no_data.extend(tree.xpath('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]/tr[2]/td[2]' + '//text()'))

    letter_no_data.extend(tree.xpath('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]/tr[3]/td[1]' + '//text()'))
    letter_no_data.extend(tree.xpath('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]/tr[3]/td[2]' + '//text()'))

    letter_no_data.extend(tree.xpath('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]/tr[4]/td[1]' + '//text()'))
    letter_no_data.extend(tree.xpath('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]/tr[4]/td[2]' + '//text()'))

    while 'WORD' in letter_no_data: letter_no_data.remove('WORD')
    for i in range(len(letter_no_data)):
        letter_no_data[i] = ''.join([j if ord(j) < 128 else ' ' for j in letter_no_data[i]])
    dates = []
    index_to_pop = []
    for i in range(len(letter_no_data) - 1):
        match = re.search(r'\d{2}/\d{2}/\d{4}', letter_no_data[i])
        if match:
            dates.append(letter_no_data[i])
            index_to_pop.append(i)
    for i in range(len(index_to_pop)):
        letter_no_data.pop(index_to_pop[i])

def get_august_twenty_one_data(tree):
    '''
    '''
    get_august_interpretive_letters(tree)
    # get_common_table_data_august('/html/body/table[2]/tr/td[2]/table/tr/td/table[1]','interpretive')
    # get_common_table_data_august('/html/body/table[2]/tr/td[2]/table/tr/td/table[2]','cra')

def get_march_twenty_ten_data(tree):
    '''
    '''
    # get the interpretive letter just in case the name changes later
    get_common_table_data_march('//*[@id="maincontent"]/table[1]','interpretive')
    get_common_table_data_march('//*[@id="maincontent"]/table[2]','corporate')
    get_common_table_data_march('//*[@id="maincontent"]/table[3]','approvals')



if __name__ == '__main__':
    '''
    '''
    # Go to start url page given in the project assignment
    driver = webdriver.Firefox()
    driver.get(START_URL)

    # click on expand all a class
    expand_all = driver.find_element_by_xpath('//*[@id="maincontent"]/div[2]/p/a[1]')
    expand_all.click()

    # with expand all clicked we need to click on All Interpretations and Actions
    all_interpretations_actions = driver.find_element_by_xpath('//*[@id="ui-accordion-2-panel-0"]/p/a')
    all_interpretations_actions.click()

    # we will store this current url because it has all the links we need
    arhieve_url = driver.current_url

    # lets go to the 2010 link
    twenty_ten_link = driver.find_element_by_xpath('//*[@id="maincontent"]/div/table/tbody/tr/td[1]/ul/li[8]/a')
    twenty_ten_link.click()

    # lets click on the march link
    march_link = driver.find_element_by_xpath('//*[@id="maincontent"]/ul/li[10]/a')
    march_link.click()

    # get the html and request data content on the page
    page = requests.get(driver.current_url)
    tree = html.fromstring(page.content)

    # get the required data needed
    get_march_twenty_ten_data(tree)

    # for faster results we'll stop using selenium now
    page = requests.get('https://www.occ.gov/static/interpretations-and-precedents/aug01/intaug01.html')
    tree = html.fromstring(page.content)

    get_august_twenty_one_data(tree)


    output_to_csv()
    driver.close()
