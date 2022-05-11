import discord

import os
import asyncio

import time
import datetime
import threading
from discord_webhook import DiscordWebhook


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from discord_webhook import DiscordWebhook
#dir_path = str(pathlib.Path(__file__).parent.absolute())
#s_path=dir_path+"/stickers/"

client = discord.Client()

#this is for heroku
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

'''
#this is for self testing
#service = ChromeService(executable_path=ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)

tee_date_url = "https://letsgo.golf/los-verdes-golf-course/teeTimes/los-verdes-golf-course-california?date=" #the url booking a specific day
all_days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"] #default values
all_times = ["6:00am","8:00am"]
book_times = {"Sunday":[["5:00pm","6:00pm"]],"Wednesday":[["5:00pm","6:00pm"]],"Saturday":[["5:00pm","6:00pm"]]}  #changed data to dict  days:[times] times = [xx:xxam-yy:yypm]
for i in all_days: #can cross out later
    book_times[i] = [all_times]
#days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"] #all default
book_list = {}
#email, password = "praiseper02@gmail.com", "Pyrian#863" personal dummy no credit
email, password = "accblues@gmail.com", "peh-pye*pxr4CEK9pry"  #cho credit
operational = "Online"
service = None 
driver = None

def p_book_times():
    for k,v in book_times.items():
        print(str(k) + ":  " + str(v))

async def message_test(date):
    #global days
    #global times
    channel = client.get_channel(845458791918469180)
    await channel.send("current time = " + str(date.strftime("%Y-%m-%d / %H:%M:%S")))
    #await channel.send("What days and times to search: \n Days: " + str(book_times.keys()) + "\n Times: " + str("6:00am - 8:00am")) # book_times.values()
    await channel.send("Booked Times: " + str(book_list)+'\n')
    await channel.send("---------")

def threading1():
    global book_times
    #global times
    global book_list
    global email
    global password

    schedule_time = datetime.datetime.now()

    #schedule_time = schedule_time.replace(hour = 0, minute = 25, second = 0) #for 9am
    #d = datetime.datetime(2009, 10, 5, 18, 00) specify to 9am?
    #date = datetime.strptime('26 Sep 2012', '%d %b %Y')
    

    #threading.Timer(10,threading1).start() #every 10 seconds, check the current time
    now = datetime.datetime.now()
    print("current time = ", now.strftime("%M:%S"))
    #p_book_times()
    
    #if time == expected time
    
    while not client.is_closed():
        now = datetime.datetime.now()
        if schedule_time  <= now: #if now.strftime("%H:$M") == ?
            schedule_time += datetime.timedelta(minutes = 5)#every 5 mins or so
            #schedule_time += datetime.timedelta(hours = 24)
            
            p_book_times()
            log_in()
            mb = url_date()
            driver.quit()
            #add one day to schedule_time to repeat on next day
            #if mb: # only send discord message if booked?
            client.loop.create_task(message_test(now))
            print("schedu looped")
        time.sleep(10)
        #print("10s")


'''
async def function():

    schedule_time = datetime.datetime.now()#(year, month, day, hour, minute, second, microsecond)
    await client.wait_until_ready()

    while not client.is_closed():
        
       now = datetime.datetime.now()
       if schedule_time  <= now:
            #JOB
            channel = client.get_channel(845458791918469180)
            await channel.send("What days and times to search: \n Days: " + str(days) + "\n Times: " + str(times))
            log_in()
            url_date()
            driver.quit()
            #add one day to schedule_time to repeat on next day
            print("schedu looped")
            schedule_time+= datetime.timedelta(minutes = 1)
       await asyncio.sleep(1)# not sure if i should set this to 20 secs example or 1 second or so delay-this is delay it takes to check every x seconds if time is right. 
'''


def time_convert(t):#converts 1pm->1:00pm
    total = []
    for i in t:
        if ":" in i:
            total.append(i)
        total.append(i[:-2]+":00"+i[-2:])
    return total

def time_within(t_ranges,t_s):#check if time is within timeframe
    #print(t_ranges,t_s)
    for time_frame in t_ranges:#changed so that will check all times and see if within list of time frames for a day. 
        tt = time_frame + [t_s] #t_range = range, t_s equals current time
        #print(tt)
        t_r = []
        #print(tt)
        for i in tt:
            
            if i[-2:] == "am": 
                t_r.append(int(i[:-5]+i[-4:-2]))
            else:
                t_r.append(int(i[:-5]+i[-4:-2])+1200)#turning into military time
        #print(t_r)
         # t_r: 0 = start, 1 = end, 2 = specific/curent time
        if t_r[0] <= t_r[2] <= t_r[1]:
            return True
    return -1


def log_in():#login after getting to right site
    global driver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://letsgo.golf/los-verdes-golf-course/login")
    driver.find_element(by = By.XPATH, value = "//*[@id='email']").send_keys(email)
    driver.find_element(by = By.XPATH, value = "//*[@id='password']").send_keys(password + Keys.ENTER)
    print(driver.current_url)
    
def url_date():#change url to manipulate date
    global book_list
    output_return = False
    WebDriverWait(driver,timeout = 30).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div"))
    x = datetime.datetime.now()
    global book_list
    for d,b in book_list:
        if datetime.datetime.strptime(d,"%Y-%m-%d")>= x:
            book_list.pop(d)
   
    for i in range(9,7,-1): #last 2 days 8,9
        y = x + datetime.timedelta(days = i)
        day_name = y.strftime("%A")
        if day_name not in book_times.keys():# if not a planned day of the week to gold, skip
            continue 
        #bcuz only testing last day, don't check which day
        y = str(y).split()
        if y[0] in book_list:#if already booked, skip over this day 
            continue #2022-04-03 in book_list
        driver.get(tee_date_url+y[0])
        #time.sleep(1) MIGHT NEED TO UNCOMMENT THIS
        try: #this is the webdriver wait/sleep 
            myElem = WebDriverWait(driver, timeout = 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/main/div/section/div[4]/div/div[1]/label")))
        except TimeoutException:
            pass
        book_list[y[0]]= book_time(book_times[day_name]) #inserting as an argument the days times
        if book_list[y[0]] != "No times available":
            output_return = True
    print("Times Booked")
    print(book_list)
    return output_return

def book_time(times: list):#check listed times for the current date #arg ["12:00pm","5:00pm"]
    print(driver.current_url)
    time.sleep(1)
    try:
        times_c = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[5]/div[2]/ul"))
        times_c = WebDriverWait(times_c,timeout = 10).until(lambda d: d.find_elements(by = By.XPATH, value = ".//li")) # the times for a day
    
        #book_list = []# [time,hole,party_size,fee,cart_fee] # fee*party_size = total 
                    #ex, ['4:10pm','18', '4', '$26.00', '+$12.50']
        for i in range(len(times_c)):#iterating through the different times(start->finish for a day)
            t = times_c[i]                  #on the first time it sees a time within range, will book and break
            tt = (t.text).split("\n")
            ttt = tt[0].replace(" ","")#3:50 pm -> 3:50pm
            tt[0] = ttt.lower()

            
            if time_within(times,tt[0]) == -1:
                continue
            elif time_within(times,tt[0]): #if t[0] == time
                t.click()#click on the time
                #print("Got here")
                rates = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/div[4]/div[2]/ul"))
                rates = rates.find_elements(by = By.TAG_NAME, value = "li")
                rates[1].click()#book rate/cart or not time #click the s2wnd one  1 == no cart, 0 == car
                
                #crossed out for testing purpose, will stop after clicking the book rate
                #time.sleep(5) #get rid of this for real
                #'''
                for n in range(2):# #increase player count + default 2 + 2 = 4
                    player_count_plus = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[1]/section/section[2]/div/button[2]/i")).click()
                    time.sleep(1)#fix this sleep for some kind of wait, problem is probably, click happens same time, find element, so the click doesnt do anything. 
                #WebDriverWait(driver,timeout = 10).until(EC.textToBePresentInElementLocated(By.xpath("//*[@id='__next']/div/main/div/section/main/div[2]/h1"), "PaymentMethods"))
                time.sleep(1)
                print("terms label wait")
                WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.CLASS_NAME, value = "custom-control-label"))
                
                #checkbox click for credit card checkbox 
                term = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/div[2]/div/div[1]/div/div/label"))
                driver.execute_script("arguments[0].click();",term)

                #checkbox click for terms agreement
                term = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[1]/div[1]/label"))
                driver.execute_script("arguments[0].click();",term)

                #final confirmation button
                book_now = WebDriverWait(driver,timeout = 10).until(lambda d: d.find_element(by = By.XPATH, value = "//*[@id='__next']/div/main/div/section/main/div[2]/section[2]/div[2]/div/button"))
                book_now.click()
                #'''
                
                return tt[0]#add the time booked to book_list to debug breaks?
                #break#get rid later
            else:
                break
        return "No times available"
    except:
        return "No times available"

@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #client.loop.create_task(function())
    t1 = threading.Thread(target=threading1)
    t1.start()

@client.event
async def on_message(message):
    #global times,days,operational
    global book_times,operational
    msg = message.content
    if message.author == client.user:
        return

    if msg.startswith('~hello'):
        await message.channel.send('Hello!')

    if msg.startswith('~help'):
        await message.channel.send('''
        Commands
        ~hello      -   hello
        ~help       -   displays commands
        ~status     -   display bot configurations(time,days,on/off)
        X~set_time   -   set time for booking(~set_time 5:00am-6:00pm)
        X~set_days   -   set days for booking(~set_day Mondays,Tuesdays)
        ~add_daytime  -   set day and time for booking ex. Monday,Tuesday,Wednesday 5:00pm-6:00pm
        ~stop       -   stop bot from booking
        ~start      -   bot resumes booking
        ''')

    if msg.startswith('~status'):
        return_string = "Times to book \n"
        for k,v in book_times.items():
            return_string += str(k) + ": " + str(v) + '\n'
        await message.channel.send(return_string + '\n' +
                                str(operational))
        
    '''#days,times = ["Sunday","Wednesday","Saturday"],["5:00pm","6:00pm"]
    if msg.startswith('set_times'): #random happy
        try:# if message is right format
            message2 = msg.split()
            times = [message2.split("-")]
            await message.channel.send("Times accepted")
        except:
            await message.channel.send("Error")
        

    if msg.startswith('~set_days'): #random something
        try:# if message is right format
            message2 = msg.split()
            days = message2[1].split(",")
            await message.channel.send("Days Accepted")
        except:
            await message.channel.send("Error")
    '''
    if msg.startswith('add_daytime'): #random something
        try:# if message is right format
            message2 = msg.split()
            days = message2[1].split(",")
            await message.channel.send("Days Accepted")
        except:
            await message.channel.send("Error")
        
    if msg.startswith('~stop'):
        operational = "offline"
    if msg.startswith('~start'):
        operational = "online"
#api_key="E20N9WNT3FMJ"








#menhera    ODQxNTYyMTQ5NzAwODk0NzIw.YJoj0w.z7PZJGgTXDADJbynZIbP9CHJuQs
#teetime OTYyMjQ1MjcxNTc4ODk4NDUy.YlEuvg.UlQBLzcVrddWKZiqP9CvOAQY_Fc
#print(os(dir_path).getenv("TOKEN"))
#print(os.getenv("TOKEN"))
#client.run(os.getenv("TOKEN"))
client.run("OTYyMjQ1MjcxNTc4ODk4NDUy.YlEuvg.UlQBLzcVrddWKZiqP9CvOAQY_Fc") # teetime
#client.run("ODQxNTYyMTQ5NzAwODk0NzIw.YJoj0w.z7PZJGgTXDADJbynZIbP9CHJuQs") # menhera

#https://discord.com/api/oauth2/authorize?client_id=841562149700894720&permissions=67584&scope=bot











