
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import easygui as eg


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://letsgo.golf/los-verdes-golf-course/teeTimeCheckout/los-verdes-golf-course-california?allCartSelected=true&allRatesSelected=true&courseName=Los%20Verdes%20Golf%20Course&date=2022-04-15&holesGroupText=18&is_riding=false&major_rate_type=regular&max_hour=21&max_price=500&min_hour=5&min_price=0&minor_rate_type=Los%20Verdes%20Public%20Times&num_holes=18&playersGroupText=2%20-%0A%20%20%20%20%20%204&qty=2&rate_type=is_regular_rate&time_slot=5%3A10%3A00%20PM&transportText=Available&transportTextRate=Unavailable")
#term = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[1]/div[1]/label"))
time.sleep(3)
term = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.ID, value = "termsAndConditions"))
term.click()







'''

from re import T
import easygui as eg



def time_inputs():
    #return mwf, and time frames
    q = "Enter the days you wish to book"
    t = "Tee_Book"
    o = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    days = eg.multchoicebox(q,t,o)
 
    times = eg.enterbox("What times to book(ex. 11:00am-1:00pm)")

    return days,times.split("-")

def time_convert(t):
    total = []
    for i in t:
        if ":" in i:
            total.append(i)
        total.append(i[:-2]+":00"+i[-2:])
    return total
a,b = time_inputs()
print(a,b)
print(time_convert(b))



tt = (t.text).split("\n")
        ttt = tt[3].replace(" ","")
        book_list.append(tt[:3]+[ttt]+[tt[4]]) #['4:10pm','18', '4', '$26.00', '+$12.50']
        print(tt[0])
        if time_within(times,book_list[-1][0]) == -1:
            continue
        elif time_within(times,book_list[-1][0]): #if t[0] == time
            t.click()
            print("Got here")
            bt = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='book_time']/div/div[3]/button[1]"))
            #print(bt.text)
            time.sleep(1)
            bt.click()#book time
            bt = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='login']/div/div[3]/div[1]/button[2]"))
            bt.click()#close

            time.sleep(1)#give time to load after exit, and set bk to the new page/refresh
            bk = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_elements(by = By.XPATH, value = "//li[contains(@class,'time-legacy')]"))

            #to do incorporate, delete break, find why text.split stale element
            #time.sleep(2)
            #for testing, will close the login/register so it will go through multiple times
        else:
            break






but1 = driver.find_element(by = By.ID, value = "page")
    but1 = but1.find_element(by = By.ID, value = "content")
    but1 = but1.find_element(by = By.CLASS_NAME, value = "btn")
    but1.click()
    time.sleep(2)

    bk = driver.find_element(by = By.ID, value = "page")
    bk = bk.find_element(by = By.ID, value = "content")
    bk = bk.find_element(by = By.ID, value = "times")


    def date_advance():

    #go 9 days ahead, check the bookings time 
    x = datetime.datetime.now()
    x+=datetime.timedelta(days = 9) #calculate day ahead date
    x = str(x).split()
    x = x[0].split("-")
    print(x)#['2022', '04', '15']

    str_date = x[1]+"-"+x[2]+"-"+x[0]
    print(str_date)#04-15-2022
    #bbut = driver.find_element(by = By.ID, value = "page")
    #bbut = bbut.find_element(by = By.ID, value = "nav")
    #new click on the date to open

    date =  WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[4]/div/div[2]/div/div[1]/div/div/div/input"))
    date.click()

    pointer = date
    print("Got the month?")
    #0)
    #time.sleep(1)
    
    #and then click the last/available date
    #month
    month =  WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[4]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div[2]/div[2]"))
    #bbut =  WebDriverWait(bbut,timeout = 10).until(lambda d: d.find_elements())
    weeks = month.find_elements(by = By.XPATH, value = ".//*")#items under month = weeks multiple
    find = False
    for w in weeks:#items in weeks = a week
        days = w.find_elements(by = By.XPATH, value = ".//*") #getting days in a week
        for d in days:
            #print(d.text) 
            if d.text == x[2]:
                find = True
                pointer = d
                d.click()
                break
        if find:
            break
    #the magnifying glass set date button
    set_date = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[4]/div/div[5]/img")) #getting days in a week
    set_date.click()
    #bbut = bbut.find_elements(by = By.XPATH, value = ".//*")
    #for e in bbut:
        #print(e.text)

    #bbut =  WebDriverWait(driver,timeout = 10).until(lambda d: d.find_elements(by = By.XPATH, value = "//td[@class='day']"))

    #bbut[-1].click()
    #time.sleep(1)#wait for the new date to load



 x = datetime.datetime.now()
    #x+=datetime.timedelta(days = 8) #calculate day ahead date
    #x = str(x).split()



    #2022-04-06
    driver.get(tee_date_url+x[0])
    time.sleep(1)



def los_button():
    #website info
    print("\nSTART")
    driver.get("https://foreupsoftware.com/index.php/booking/20330/4502#/teetimes")
    #time.sleep(2)
    but1 = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='content']/div/h3/a/img"))

    but1.click()

    time.sleep(3)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    print("FIN\n")


'''