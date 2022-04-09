#import pytest
from argparse import Action
import time
import datetime
from tkinter import Y

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import action_builder
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import easygui as eg
#import tkinter as tk
#from tkinter import simpledialog

#setup


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

tee_date_url = "https://letsgo.golf/los-verdes-golf-course/teeTimes/los-verdes-golf-course-california?date=" #the url booking a specific day
days,times = ["Sunday","Wednesday","Saturday"],["5:00pm","6:00pm"]
book_list = []


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




def log_in():#login after getting to right site
    driver.get("https://letsgo.golf/los-verdes-golf-course/login")
    #li = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/div/div/div[2]/a[1]"))
    #li.click()
    driver.find_element(by = By.XPATH, value = "//*[@id='email']").send_keys("praiseper02@gmail.com")
    driver.find_element(by = By.XPATH, value = "//*[@id='password']").send_keys("Pyrian#863" + Keys.ENTER)

def date_in():
    return "date" in driver.current_url


def url_date():#change url to manipulate date
    
    WebDriverWait(driver,timeout = 30).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div"))

    x = datetime.datetime.now()

    book_list = [d for d in book_list if d[0] >= x]#delete booked dates from old. 

    for i in range(0,10): #9 days in advance
        y = x + datetime.timedelta(days = i)
        print(y.strftime("%A"))
        if y.strftime("%A") not in days:# if not a planned day of the week to gold, skip
            continue
        y = str(y).split()
        if y[0] in [x[0][0] for x in book_list]:#if already booked, skip over this day
            continue

        print(y,"y here")
        driver.get(tee_date_url+y[0])
        time.sleep(1)
        try:
            myElem = WebDriverWait(driver, timeout = 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/main/div/section/div[4]/div/div[1]/label")))
            print("Page is ready!")#wide-search-area wide-search-are-border By.XPATH, 
        except TimeoutException:
            print("Loading took too much time!")
        #time.sleep(1)
        
        book_list.append([y,book_time()])


    print(book_list)




    

        

def book_time():#check listed times for the current date #arg ["12:00pm","5:00pm"]
    
    times_c = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[5]/div[2]/ul"))
    times_c = times_c.find_elements(by = By.XPATH, value = ".//li") # the times for a day
    #book_list = []# [time,hole,party_size,fee,cart_fee] # fee*party_size = total 
                #ex, ['4:10pm','18', '4', '$26.00', '+$12.50']
    print("book time start")
    for i in range(len(times_c)):#iterating through the different times(start->finish for a day)
        t = times_c[i]                  #on the first time it sees a time within range, will book and break
        tt = (t.text).split("\n")
        ttt = tt[0].replace(" ","")#3:50 pm -> 3:50pm
        tt[0] = ttt.lower()
        
        print(tt[0])
        
        if time_within(times,tt[0]) == -1:
            continue
        elif time_within(times,tt[0]): #if t[0] == time
            t.click()#click on the time
            #print("Got here")
            rates = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[4]/div[2]/ul"))
            rates = rates.find_elements(by = By.XPATH, value = ".//*")
            #print(bt.text)
            #time.sleep(1)
            rates[1].click()#book rate/cart or not time #click the s2wnd one

            #time.sleep(30)#onto payment confirmation page, not refresh

            #increase player count +
            for n in range(2):# default 2 + 2 = 4
                player_count_plus = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[1]/section/section[2]/div/button[2]/i")).click()
                time.sleep(1)#fix this sleep for some kind of wait, problem is probably, click happens same time, find element, so the click doesnt do anything. 
            #WebDriverWait(driver,timeout = 10).until(EC.textToBePresentInElementLocated(By.xpath("//*[@id='__next']/div/main/div/section/main/div[2]/h1"), "PaymentMethods"))
           
            print("player count")
            time.sleep(1)
            #terms confirm
            term = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[1]/div[1]/label"))
            driver.execute_script("arguments[0].click();",term)
            #print("terms")

                       
           


            #final confirmation button
            book_now = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[2]/div/button"))
            book_now.click()
            #after this, it should go to a whats booked page
            #so proba can go back to url dates to start the booking time over again

            #don't know how to exit/go back because need log in
            return tt[0]#add the time booked to book_list to debug
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

log_in()
url_date()

#date_advance()#dates to click on (days)
#book_time(times)#timeframes to book
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


















