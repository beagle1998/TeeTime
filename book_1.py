#import pytest
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import easygui as eg
#import tkinter as tk
#from tkinter import simpledialog

#setup


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def time_convert(t):#converts 1pm->1:00pm
    total = []
    for i in t:
        if ":" in i:
            total.append(i)
        total.append(i[:-2]+":00"+i[-2:])
    return total

def time_inputs(): #asks user for time inputs
    #return mwf, and time frames
    q = "Enter the days you wish to book"
    t = "Tee_Book"
    o = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    days = eg.multchoicebox(q,t,o)
 
    times = eg.enterbox("What times to book(ex. 11:00am-1:00pm)")

    return days,time_convert(times.split("-"))


def time_within(t_range,t_s):#check if time is within timeframe
    tt = t_range + [t_s]
    print(tt)
    t_r = []
    for i in tt:
        
        if i[-2:] == "am": 
            t_r.append(int(i[:-5]+i[-4:-2]))
        else:
            t_r.append(int(i[:-5]+i[-4:-2])+1200)
    print(t_r)
    if t_r[2] < t_r[0]:
        return -1
    return t_r[0] <= t_r[2] <= t_r[1]


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


def log_in():#login after getting to right site
    li = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/div/div/div[2]/a[1]"))
    li.click()

def url_date():#change url to manipulate date
    url = driver.current_url
    print(url)
    #&date=2022-04-18
   
    d = url.index("date")

    x = datetime.datetime.now()
    x+=datetime.timedelta(days = 9) #calculate day ahead date
    x = str(x).split()
    #x = x[0].split("-")

    print(x)#['2022', '04', '15']
    url = url[:d+4] + x[0] 
    print(url)
    driver.get(url)
    time.sleep(1)




    
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
    time.sleep(1)#wait for the new date to load


        

def book_time(times):#check listed times for the current date #arg ["12:00pm","5:00pm"]

    times_c = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[5]/div[2]/ul"))
    times_c = times_c.find_elements(by = By.XPATH, value = ".//li") # the times for a day
    book_list = []# [time,hole,party_size,fee,cart_fee] # fee*party_size = total 
                #ex, ['4:10pm','18', '4', '$26.00', '+$12.50']
    print("book time start")
    for i in range(len(times_c)):#iterating through the different times(start->finish for a day)
        #print(i,"I range")
        t = times_c[i]
        #print(t.text)
        time.sleep(1)
        #print(t.text)
        tt = (t.text).split("\n")
        print(tt)
        ttt = tt[0].replace(" ","")#3:50 pm -> 3:50pm
        tt[0] = ttt.lower()
        book_list.append(tt)
        print(tt[0])
        
        if time_within(times,tt[0]) == -1:
            continue
        elif time_within(times,tt[0]): #if t[0] == time
            t.click()#click on the time
            print("Got here")
            rates = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[4]/div[2]/ul"))
            rates = rates.find_elements(by = By.XPATH, value = ".//*")
            #print(bt.text)
            time.sleep(1)
            rates[1].click()#book rate/cart or not time #click the s2wnd one

            time.sleep(30)#onto payment confirmation page, not refresh

            '''
            #increase player count +
           # player_count_plus = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[1]/section/section[2]/div/button[2]/i"))
           # player_count_plus.click()
           # time.sleep(1)

            term = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[1]/div[1]/label"))
            term.click()

            #final confirmation button
            book_now = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[2]/div/button"))
            book_now.click()
            '''
            #don't know how to exit/go back because need log in
            break#get rid later
        else:
            break
        
        #ttt = tt[3].replace(" ","")
    #print(book_list)

    #with the specified time frame/time slot, find if it has.
    #ex. 5 pm
    
        
    

#arguments 
# days of the week #0-7
# time frames # 9:00am-1:00pm

#days,times = time_inputs()#asks user for input of dayts,time
#for now use static inputs
days,times = ["Sunday","Wednesday","Saturday"],["5:00pm","6:00pm"]

los_button()

#log_in()
#url_date()

date_advance()#dates to click on (days)
book_time(times)#timeframes to book
time.sleep(30)
#sleep/give time to see
#time.sleep(5)
#driver.quit() #quit

'''
framework

#access the link https://foreupsoftware.com/index.php/booking/20330/4502#/teetimes

#start at 9am
-click on the middle to access the bookings
-find and click on the date+9
check the earliest booking, if its within a certain timeframe, book it?
#beat capcha
#booktime button

#notes
#assume already logged in

'''


















