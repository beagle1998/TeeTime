import pytest
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
    #print(tt)
    t_r = []
    for i in tt:
        
        if i[-2:] == "am": 
            t_r.append(int(i[:-5]+i[-4:-2]))
        else:
            t_r.append(int(i[:-5]+i[-4:-2])+1200)
    #print(t_r)
    if t_r[2] < t_r[0]:
        return -1
    return t_r[0] <= t_r[2] <= t_r[1]


def los_button():
    #website info
    print("\nSTART")
    driver.get("https://foreupsoftware.com/index.php/booking/20330/4502#/teetimes")
    #time.sleep(2)
    but1 = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='content']/div/button"))

    but1.click()
    #driver.refresh()
    print("FIN\n")

def date_advance():

    #go 9 days ahead, check the bookings time 
    x = datetime.datetime.now()
    x+=datetime.timedelta(days = 9) #calculate day ahead date
    x = str(x).split()
    x = x[0].split("-")
    str_date = x[1]+"-"+x[2]+"-"+x[0]

    #bbut = driver.find_element(by = By.ID, value = "page")
    #bbut = bbut.find_element(by = By.ID, value = "nav")
    
    bbut =  WebDriverWait(driver,timeout = 10).until(lambda d: d.find_elements(by = By.XPATH, value = "//td[@class='day']"))

    bbut[-1].click()
    time.sleep(1)#wait for the new date to load


        

def book_time(times):#check listed times for the current date #arg ["12:00pm","5:00pm"]

    bk = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_elements(by = By.XPATH, value = "//li[contains(@class,'time-legacy')]"))

    book_list = []# [time,hole,party_size,fee,cart_fee] # fee*party_size = total 
                #ex, ['4:10pm','18', '4', '$26.00', '+$12.50']
    
    for i in range(len(bk)):
        #print(i,"I range")
        t = bk[i]
        #print(t.text)
        time.sleep(1)
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


















