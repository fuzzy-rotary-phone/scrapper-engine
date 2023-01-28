import json
import yaml
import time
# from selenium import webdriver
from seleniumwire import webdriver
from seleniumwire.utils import decode
# from selenium.webdriver.chrome import Options
# from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By

DOWNLOAD_DIR = './download/zoominfo/'
CHROME_DRIVER_PATH = './chromedriver'
ZOOMINFO_LOGIN_URL = 'http://login.zoominfo.com'
APP_ZOOMINFO_URL = 'https://app.zoominfo.com/#/apps/search/v2/results/person?query=eyJmaWx0ZXJzIjp7InBhc3RQb3NpdGlvbiI6W3siZCI6IkN1cnJlbnQgQ29tcGFueSIsInYiOiIxIn1dLCJpc0NlcnRpZmllZCI6W3siZCI6IkNlcnRpZmllZCBBY3RpdmUgQ29tcGFuaWVzIE9ubHkiLCJ2Ijp0cnVlfV0sInNvcnRQZW9wbGUiOlt7ImQiOiJSZWxldmFuY2UiLCJ2IjoiUmVsZXZhbmNlIiwiaXNEZWZTcnQiOnRydWV9XSwic29ydFBlb3BsZU9yZGVyIjpbeyJkIjoiIiwidiI6ImRlc2MifV0sInNvcnRDb21wYW55IjpbeyJkIjoiUmVsZXZhbmNlIiwidiI6IiIsImlzRGVmU3J0Ijp0cnVlfV0sInNvcnRDb21wYW55T3JkZXIiOlt7ImQiOiIiLCJ2IjoiZGVzYyJ9XSwic29ydFNjb29wIjpbeyJkIjoiIiwidiI6IiIsImlzRGVmU3J0Ijp0cnVlfV0sInNvcnRTY29vcE9yZGVyIjpbeyJkIjoiIiwidiI6ImRlc2MifV0sImJvYXJkTWVtYmVycyI6W3siZCI6IkV4Y2x1ZGUgQm9hcmQgTWVtYmVycyIsInYiOjB9XSwicGFydGlhbFByb2ZpbGVzIjpbeyJkIjoiRXhjbHVkZSBQYXJ0aWFsIFByb2ZpbGVzIiwidiI6dHJ1ZX1dLCJleGNsdWRlRGVmdW5jdENvbXBhbmllcyI6W3siZCI6IkV4Y2x1ZGUgRGVmdW5jdCBDb21wYW5pZXMiLCJ2Ijp0cnVlfV0sIm5lZ2F0aW9uIjpbeyJkIjoiIiwidiI6ZmFsc2V9XSwiY29udGFjdEluZm8iOlt7ImQiOiJBbnkgSW5mbyIsInYiOiIifV0sImV4Y2x1ZGVFeHBvcnRlZENvbnRhY3RzIjpbeyJkIjoiIiwidiI6ZmFsc2V9XSwiZXhjbHVkZUV4cG9ydGVkQ29tcGFuaWVzIjpbeyJkIjoiIiwidiI6ZmFsc2V9XSwiZXhjbHVkZUltcG9ydGVkQ29tcGFuaWVzIjpbeyJkIjoiIiwidiI6ZmFsc2V9XSwiZXhjbHVkZUltcG9ydGVkQ29udGFjdHMiOlt7ImQiOiIiLCJ2IjpmYWxzZX1dLCJjb25maWRlbmNlUmFuZ2UiOlt7ImQiOiI4NS05OSIsInYiOls4NSw5OV19XSwib3V0cHV0Q3VycmVuY3lDb2RlIjpbeyJkIjoiIiwidiI6IlVTRCJ9XSwiaW5wdXRDdXJyZW5jeUNvZGUiOlt7ImQiOiIiLCJ2IjoiVVNEIn1dLCJtZXRyb1JlZ2lvbiI6W3siZCI6IkNBIC0gTG9zIEFuZ2VsZXMiLCJ2IjoiQ0EgLSBMb3MgQW5nZWxlcyJ9LHsiZCI6IkNBIC0gU2FuIEZyYW5jaXNjbyIsInYiOiJDQSAtIFNhbiBGcmFuY2lzY28ifSx7ImQiOiJHQSAtIEF0bGFudGEiLCJ2IjoiR0EgLSBBdGxhbnRhIn0seyJkIjoiTlkgLSBOZXcgWW9yayIsInYiOiJOWSAtIE5ldyBZb3JrIn0seyJkIjoiV0EgLSBTZWF0dGxlIiwidiI6IldBIC0gU2VhdHRsZSJ9XSwiaW5kdXN0cnlDbGFzc2lmaWNhdGlvbiI6W3siZCI6IkJhcmJlciBTaG9wcyAmIEJlYXV0eSBTYWxvbnMiLCJ2IjoiY29uc3VtZXJzZXJ2aWNlcy5oYWlyc2Fsb24ifSx7ImQiOiJSZXN0YXVyYW50cyIsInYiOiJob3NwaXRhbGl0eS5yZXN0YXVyYW50In0seyJkIjoiSG9zcGl0YWxzICYgUGh5c2ljaWFucyBDbGluaWNzIiwidiI6Imhvc3BpdGFscyJ9XSwiZW1wbG95ZWVzQ291bnQiOlt7ImQiOiJBYm92ZSA1MCIsInYiOlsiNTAiLCIxMEsrIl19XSwicmV2ZW51ZVJhbmdlIjpbeyJkIjoiQWJvdmUgJDEwTSIsInYiOlsiJDEwTSIsIiQ1QisiXX1dLCJtYW5hZ2VtZW50TGV2ZWwiOlt7ImQiOiJDLUxldmVsIiwidiI6IkNfRVhFQ1VUSVZFUyJ9LHsiZCI6IlZQLUxldmVsIiwidiI6IlZQX0VYRUNVVElWRVMifSx7ImQiOiJEaXJlY3RvciIsInYiOiJESVJFQ1RPUiJ9XX0sInNlYXJjaFR5cGUiOjAsImljcFN0YXR1cyI6dHJ1ZSwiZGVmYXVsdEljcFByb2ZpbGUiOm51bGwsInNraXBIaXN0b3J5IjpmYWxzZSwicGFnZSI6Mn0%3D'
APP_ZOOMINFO_SEARCH_URL = 'https://app.zoominfo.com/#/apps/search/v2/saved'
COOKIES = '_cfuvid=qDqo.PWm5.c4QD1pwMXpWFUYmHOmJvYRivLKZtbLja8-1674733362509-0-604800000; __cf_bm=V3lg1TxgabMaXUwwG3ttW6lDgOj0H8MOTz9D_fBeY0M-1674733363-0-Af0FnXaclL5cKx1s34yp8RH9agXezeny0hQjfqjxN6OZ6GofzQ7DNG5z29d0avG7W5I/aJzDJNVcPZ8vRsFFCps=; pxcts=8c59d530-9d6e-11ed-a195-526e416c4449; _pxvid=8b65fb09-9d6e-11ed-aa50-50626a775a4f; _gcl_au=1.1.1268648508.1674733366; _ga=GA1.2.1497276385.1674733369; _gid=GA1.2.129575799.1674733369; doziUser=srikarraj@chillpanda.in; oktaMachineId=10e2ec4e-9ae3-e373-0afe-e79021d1423f; userEmail=srikarraj@chillpanda.in; email=srikarraj@chillpanda.in; name=Srikar Raj chakilam; firstname=Srikar; userZoomCompanyId=20408085; analyticsId=31318738; userEmail=srikarraj@chillpanda.in; DontShowExpiringSubscriptionDialog=true; totango.heartbeat.last_module=DOZI; ziid=TVeORzN7CFbxqxXQmhZSEd9V0mu2W0bqDfG-OTcz0uGV49QGdQsSf9wI-ItUZR77X-NMf4UbnOIrGbidxzytKQ; zisession=TVeORzN7CFbxqxXQmhZSEd9V0mu2W0bqDfG-OTcz0uGV49QGdQsSf9wI-ItUZR77X-NMf4UbnOIHZfBdsIRZTw3SGGWHjsOYHpTlaIV_kK77hKuMdT8meabersyAvwk0; ziaccesstoken=eyJraWQiOiJGaWtfUWFxeklaOUtFY0hrMW8tOURDblBaUU9iM29YaTczSG5FMlVOU1lNIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmhYN3dZME43SmN6Z2hRWnptLWVka2hZOEdydkZKRFZ3S1JrbE5kU214UmsiLCJpc3MiOiJodHRwczovL29rdGEtbG9naW4uem9vbWluZm8uY29tL29hdXRoMi9kZWZhdWx0IiwiYXVkIjoiYXBpOi8vZGVmYXVsdCIsImlhdCI6MTY3NDczMzgwMiwiZXhwIjoxNjc0Nzg3ODAyLCJjaWQiOiIwb2E5OWRzbWJuQXhsZXZGMzY5NiIsInVpZCI6IjAwdTN4MHRvdGR3aVFnTlVhNjk3Iiwic2NwIjpbImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSJdLCJhdXRoX3RpbWUiOjE2NzQ3MzM4MDEsInppVXNlcm5hbWUiOiJzcmlrYXJyYWpAY2hpbGxwYW5kYS5pbiIsInN1YiI6InNyaWthcnJhakBjaGlsbHBhbmRhLmluIiwiZmlyc3ROYW1lIjoiU3Jpa2FyIiwibGFzdE5hbWUiOiJSYWogY2hha2lsYW0iLCJ6aVNlc3Npb25UeXBlIjotMywiemlHcm91cElkIjowLCJ6aVVzZXJJZCI6MzEzMTg3MzgsInppVGVuYW50SWQiOjIwNDA4MDg1LCJlbWFpbCI6InNyaWthcnJhakBjaGlsbHBhbmRhLmluIiwic2ZBY2NvdW50SWQiOiIwMDFEbzAwMDAwN1VFZnpJQUciLCJ6aU1vbmdvVXNlcklkIjoiMzEzMTg3MzgiLCJ6aVBsYXRmb3JtcyI6WyJET1pJIiwiQURNSU4iXX0.TlaXrrdoaZlRJ9tK8G4KlGS9GIYV5ahSxuGvEBMbe_chVe9y8gXv8e9Tzp8F06_DGfJ0sOt2ggp48cUqexXQcT8xEoyZNIniNlSkWksIKMQniHEtZfnN5bwPNYKD3GRrMVahiY72dUoJkZJHb2TkVnTnpnJ8npbeiLceqPI84GWmOa_Rnad-qYjv3GLc4MX5m5GooH8H6Nwfa23ZKADrKSBGJTCg7gBFckLBXTGrKQjWcXyFAv-8y-OzCuPvEjBwdEWhmnjusPqBuwGfLRRaYwgKsOCMzi80rdbOEPhV4mc7ovDXtsEC7ThSPL2GzVgNrJIxjlGwxFaQ59o4V8WQXA; parseSessionToken=1; userId=31318738; amplitude_id_b497e086f6cb3da6baca4fcfa0bb09e8_engageamplitudezoominfo.com=eyJkZXZpY2VJZCI6IjAwY2YwM2RlLWVjNDAtNGRmNS05ZWM1LWNmZjJhYTg3ZWQ0Y1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY3NDczMzU0MjQ1NCwibGFzdEV2ZW50VGltZSI6MTY3NDczMzgxNDgyMCwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; _px3=d358f5d49144d01d4d3cd3628feaa455be9bf35c1975d04f400f4a18a526b97d:2CIry7xxyiQgcnta/4X9uJb6X0lJNWpLm9W5XqD9W3Cw1y9gE8gCjNrWLgeWx7Xg5zlQNOAVxThDEe/pvdyP8A==:1000:eb4QnzFnJkBEaMzDLhSStXvkueF8y9Ggpq61B4ao6LennsWpBFJy7ywZMMILiHdriDfGYLGB3Q7SR8HCCvR5YCvq3wNfhpHLUVaC2mxy5WF2vNNKVu1RGyAwPZv6KDNSwMILX/l6iYmJSO4AkfZ3T2XnyqNNPIDSfuZzGIFDgmuQRhPGz9BwZ39Ms+nMO4sNZRiiiq+rRI/7OHQ18w/wyA==; totango.heartbeat.last_ts=1674733996129; amplitude_id_14ff67f4fc837e2a741f025afb61859czoominfo.com=eyJkZXZpY2VJZCI6ImZkMTdmZWQ0LTQwNTgtNDdkZi04YWRhLWFhMGNmNTA3NjNiYlIiLCJ1c2VySWQiOiIzMTMxODczOCIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY3NDczMzM2NTQ2MywibGFzdEV2ZW50VGltZSI6MTY3NDczNDAwNTA3MCwiZXZlbnRJZCI6MjU5LCJpZGVudGlmeUlkIjo2LCJzZXF1ZW5jZU51bWJlciI6MjY1fQ==; _dd_s=rum=0&expire=1674734937736'
# OUTPUT_FILENAME = 'zoominfo-advancedsearch'
OUTPUT_FILENAME = 'salons-search-people'
# OUTPUT_FILENAME = 'restaurants-SF-people'
# OUTPUT_FILENAME = 'restaurants-NY-people'
# OUTPUT_FILENAME = 'restaurants-LA-people'
# OUTPUT_FILENAME = 'zoominfo-restaurant-companies'
# OUTPUT_FILENAME = 'restaurants-Europe-companies'
# OUTPUT_FILENAME = 'salons-restaurants-Europe-C-level'
# OUTPUT_FILENAME = 'salons-US-VP-level'
ITEM = 3

emailId = 'okta-signin-username'
passwordId = 'okta-signin-password'
submitId = 'okta-signin-submit'
otpId = 'input81'
verifySubmitClass = 'button.button-primary'
verifyBtnXpath = "//input[@class='button button-primary']"
popupOKBtnId = 'btn-ok'
advancedSearchBtnXpath = "//button[@class='zic-advanced-search-item ng-star-inserted']"
searchDivId = 'zi-dooten-text-Search-1'
searchPeopleRequestURL = '/anura/zoominfo/hPeopleSearch'
searchCompaniesRequestURL = '/anura/zoominfo/hUnifiedCompaniesSearch'
personDetailsRequestURL = '/profiles/graphql/personDetails'
companyDetailsRequestURL = '/profiles/graphql/companyDetails'
searchContactRequestURL = '/anura/userData/viewContacts'
paginationBtnXpath = "//button[@class='p-ripple p-element p-paginator-page p-paginator-element p-link ng-star-inserted']"
paginationNextBtnXpath = "//button[@class='p-ripple p-element p-paginator-next p-paginator-element p-link']"
searchesDivXpath = "//div[@class='list ng-star-inserted']"
searchesDivXpath = "//zi-dotten-text[@class='name dotten-text']"
searchesRowXpath = "//tbody//tr"
peopleSearchId = 'people-search'

def get_browser():
    # options = Options()
    # options.add_argument("start-maximized")
    # options.add_experimental_option("detach", True)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("detach", True)
    prefs = {'download.default_directory': DOWNLOAD_DIR}
    options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    return driver

def format_json(filename):
    f = open(filename)
    jd = json.loads(f.read())
    f = open(filename + '-formatted', 'w')
    f.write(json.dumps(jd, indent=4))
    f.close()

def searchScrape(browser, company=False):
    if(not(company)):
        browser.find_element_by_id(peopleSearchId).click()
        time.sleep(30)

    first = False
    #First page scrape
    if first:
        f = open(OUTPUT_FILENAME, 'w')
        if company:
            request = browser.wait_for_request(searchCompaniesRequestURL, timeout=30)
        else:
            request = browser.wait_for_request(searchPeopleRequestURL, timeout=30)
        body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        # print(body)
        f.write(body.decode())
        f.write(',\n')
        f.close()
        del browser.requests

    time.sleep(30)
    paginationButtons = browser.find_elements_by_xpath(paginationBtnXpath)
    # print(paginationButtons)
    startPage = 8
    numClicks = 110

    for i in range(2, startPage):
        browser.find_element_by_xpath(paginationNextBtnXpath).click()
    
    for i in range(startPage, startPage + numClicks):
        # paginationButtons[i-1].click()
        browser.find_element_by_xpath(paginationNextBtnXpath).click()
        if company:
            request = browser.wait_for_request(searchCompaniesRequestURL, timeout=30)
        else:
            request = browser.wait_for_request(searchPeopleRequestURL, timeout=30)
        body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        f = open(OUTPUT_FILENAME, 'a')
        f.write(body.decode())
        f.write(',\n')
        f.close()
        print('DONE: Page ' + str(i))
        del browser.requests

    time.sleep(100)

def searchContactScrape(browser):
    browser.find_element_by_id(peopleSearchId).click()
    time.sleep(10)

    rows = browser.find_elements_by_xpath(searchesRowXpath)
    print(len(rows))
    f1 = open(OUTPUT_FILENAME + '-personaldetails', 'a')
    # f2 = open(OUTPUT_FILENAME + '-companydetails', 'a')
    f3 = open(OUTPUT_FILENAME + '-contacts', 'a')

    if not rows:
        print('Error: No rows')

    first = True

    if first:
        for i in range(0, 25):
            browser.find_element_by_xpath(searchesRowXpath + '[' + str(i+1) + ']//td[3]').click()
            request1 = browser.wait_for_request(personDetailsRequestURL)
            # request2 = browser.wait_for_request(companyDetailsRequestURL)
            request3 = browser.wait_for_request(searchContactRequestURL)
            body1 = decode(request1.response.body, request1.response.headers.get('Content-Encoding', 'identity'))
            # body2 = decode(request2.response.body, request2.response.headers.get('Content-Encoding', 'identity'))
            body3 = decode(request3.response.body, request3.response.headers.get('Content-Encoding', 'identity'))
            f1.write(body1.decode())
            # f2.write(body2.decode())
            f3.write(body3.decode())
            f1.write(',\n')
            # f2.write(',\n')
            f3.write(',\n')
            browser.find_element_by_xpath(searchesRowXpath + '[' + str(i+1) + ']//td[3]').click()
            del browser.requests
            # time.sleep(10)

    f1.close()
    # f2.close()
    f3.close()

    # time.sleep(30)

    paginationButtons = browser.find_elements_by_xpath(paginationBtnXpath)
    startPage = 2
    numClicks = 100

    for i in range(2, startPage):
        browser.find_element_by_xpath(paginationNextBtnXpath).click()
    
    for j in range(startPage, startPage + numClicks):
        browser.find_element_by_xpath(paginationNextBtnXpath).click()
        rows = browser.find_elements_by_xpath(searchesRowXpath)
        f1 = open(OUTPUT_FILENAME + '-personaldetails', 'a')
        # f2 = open(OUTPUT_FILENAME + '-companydetails', 'a')
        f3 = open(OUTPUT_FILENAME + '-contacts', 'a')
        time.sleep(10)

        for i in range(25):
            browser.find_element_by_xpath(searchesRowXpath + '[' + str(i+1) + ']//td[3]').click()
            request1 = ''
            request2 = ''
            request3 = ''
            try:
                request1 = browser.wait_for_request(personDetailsRequestURL, timeout=30)
            except:
                print('Skipped personalDetails: ' + str(i))
                pass
            # try:
            #     request2 = browser.wait_for_request(companyDetailsRequestURL, timeout=30)
            # except:
            #     print('Skipped companyDetails: ' + str(i))
            #     pass
            try:
                request3 = browser.wait_for_request(searchContactRequestURL, timeout=30)
            except:
                print('Skipped contactDetails: ' + str(i))
                pass

            if request1:
                body1 = decode(request1.response.body, request1.response.headers.get('Content-Encoding', 'identity'))
                f1.write(body1.decode())
                f1.write(',\n')
            # if request2:
            #     body2 = decode(request2.response.body, request2.response.headers.get('Content-Encoding', 'identity'))
            #     f2.write(body2.decode())
            #     f2.write(',\n')
            if request3:
                body3 = decode(request3.response.body, request3.response.headers.get('Content-Encoding', 'identity'))
                f3.write(body3.decode())
                f3.write(',\n')
            
            browser.find_element_by_xpath(searchesRowXpath + '[' + str(i+1) + ']//td[3]').click()
            del browser.requests
        
        f1.close()
        # f2.close()
        f3.close()
    
        if j%5 == 0:
            time.sleep(30)
        print('DONE: Page ' + str(j))


def login():
    conf = yaml.load(open('login.yml'), Loader=yaml.Loader)
    email = conf['zoominfo']['email']
    password = conf['zoominfo']['password']
    # email = conf['zoominfo']['email1']
    # password = conf['zoominfo']['password1']

    browser = get_browser()
    browser.get(ZOOMINFO_LOGIN_URL)
    # cookiesList = COOKIES.split(';')
    # for c in cookiesList:
    #     l = c.split('=', 1)
    #     browser.add_cookie({'name': l[0], 'value' : l[1]})
        
    time.sleep(5)
    # browser.find_element(By.ID, emailId).send_keys(email)
    # browser.find_element(By.ID, passwordId).send_keys(password)
    # browser.find_element(By.ID, submitId).click()
    browser.find_element_by_id(emailId).send_keys(email)
    browser.find_element_by_id(passwordId).send_keys(password)
    browser.find_element_by_id(submitId).click()

    time.sleep(60)
    otp = input("Enter OTP:")
    browser.find_element_by_id(otpId).send_keys(str(otp))
    browser.find_element_by_xpath(verifyBtnXpath).click()

    time.sleep(60)
    browser.find_element_by_id(popupOKBtnId).click()
    time.sleep(3)
    # browser.find_element_by_xpath(advancedSearchBtnXpath).click()
    # time.sleep(5)
    # browser.find_element_by_id(searchDivId).click()
    searchDivs = browser.find_elements_by_xpath(searchesDivXpath)
    searchDivs[ITEM].click()
    time.sleep(10)

    searchScrape(browser)
    # searchScrape(browser, True)
    # searchContactScrape(browser)

    # time.sleep(100)
    # browser.close()

login()
# format_json(OUTPUT_FILENAME)